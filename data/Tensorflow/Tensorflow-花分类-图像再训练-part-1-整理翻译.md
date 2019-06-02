图像识别往往包含数以百万计的参数，从头训练需要大量打好标签的图片，还需要大量的计算力（往往数百小时的GPU时间）。对此，迁移学习是一个捷径，他可以在已经训练好的相似工作模型基础上，继续训练新的模型。

这里我们将基于ImageNet训练好的模型，对适当数量（数千张）图像进行训练，这个训练可能需要30分钟左右。
![](imgs/4324074-33eae31d3e195094.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---
##准备工作

安装tensorflow-hub,这是一个类似于tensorflow模型市场集散地的应用，这个练习将使用它的一个模型作为基础模型。
安装命令:

```
pip3 install --upgrade tensorflow-hub
```

从[百度网盘下载再训练需要使用的花图片集](https://pan.baidu.com/s/1peJ568BGJjS7UxnANzW0XQ)(密码:lzjg)

下载后解压，得到几个文件夹，分别包含了菊花daisy、蒲公英dandelion、玫瑰rose、向日葵sunflow和郁金香tulips各种花的图片，总计有几千张。

---
##读取图片列表create_image_lists

将菊花、蒲公英等各种文件夹下的图片路径都读取出来，再把每个分类的图片按照训练70%、测试20%、验证10%的比例拆分，组合成字典格式:
```
{
    dir: name, 
    trainging: [imgage_paths],
    testing: [imgage_paths], 
    validation: [imgage_paths]
}
```
为了将图片按照70%20%10%进行分类，这里使用的方法是哈希化文件名：
* 将文件名转为hash值（40个数字字母组合）
* 再把hash值转为整数（非常大的数字）
* 利用取余数运算%MAX把大整数放缩到0~MAX之间
* 0-MAX再除以MAX得到0-1随机小数，再乘以100得到百分数
* 判断这个百分数属于哪一段，就把文件名归到哪一段

以下是代码及注解，很长，耐心看：
```
import argparse
import collections
from datetime import datetime
import hashlib
import random
import re
import sys

import os
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

dir_path = os.path.dirname(os.path.realpath(__file__))
image_dir=os.path.join(dir_path,'flower_photos')  

MAX_IPC = 2 ** 27 - 1 #每分类最大图片数max-image-per-class

#要使用的hub模型，就是module_name
HUB_MODULE='https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/feature_vector/1'

#hub模型中要使用的量化操作节点名
FAKE_QUANT_OPS = ('FakeQuantWithMinMaxVars',
                  'FakeQuantWithMinMaxVarsPerChannel')


def create_image_lists():   
    result = collections.OrderedDict() #有序字典，匹配顺序到labels
    sub_dirs = sorted(x[0] for x in tf.gfile.Walk(image_dir)) #获得花类型文件夹列表，第一个是根目录    
    
    is_root_dir = True
    for sub_dir in sub_dirs:        
        if is_root_dir: #跳过根目录
            is_root_dir = False
            continue
            
        extensions = ['jpg', 'jpeg', 'JPG', 'JPEG']
        file_list = []
        dir_name = os.path.basename(sub_dir) #得到花分类的名字daisy，rose...
        if dir_name == image_dir:
            continue
        for extension in extensions:
            file_glob = os.path.join(image_dir, dir_name, '*.' + extension) #获取所有图片路径
            file_list.extend(tf.gfile.Glob(file_glob)) #将所有图片路径加入到file_list  
        label_name = re.sub(r'[^a-z0-9]+', ' ', dir_name.lower()) #清理花分类名称字符，这里没意义
        
        training_images = [] #用于训练的图片路径
        testing_images = [] #用于测试的图片路径
        validation_images = [] #用于验证的图片路径
        for file_name in file_list:
            base_name = os.path.basename(file_name) #得到文件名7166550328_de0d73cfa9.jpg...
            hash_name = re.sub(r'_nohash_.*$', '', file_name) #得到图片全路径
            hash_name_hashed = hashlib.sha1(tf.compat.as_bytes(hash_name)).hexdigest() #转40位hash
            hash_int=int(hash_name_hashed, 16) #转超长的整数
            hash_per=hash_int%(MAX_IPC + 1)*(100.0 / MAX_IPC) #放缩到0~100

            if hash_per < 10: #验证集10%
                validation_images.append(base_name)
            elif hash_per < 30: #测试集20%
                testing_images.append(base_name)
            else: #训练集70%
                training_images.append(base_name)
                
        result[label_name] = {
            'dir': dir_name,
            'training': training_images,
            'testing': testing_images,
            'validation': validation_images,
        }
    return result

#入口函数
def main(_):    
    create_image_lists();

#模块或应用
if __name__ == '__main__':
    tf.app.run()
```

最终输出的result格式：
```
([
    ('daisy', { 
        'dir': 'daisy', 
        'training': ['14167534527_781ceb1b7a_n.jpg',...], 
        'testing': ['20773528301_008fcbc5a1_n.jpg',...],
        'validation': ['721595842_bacd80a6ac.jpg',...]
    }), 
    ('dandelion', { 
        'dir': 'dandelion', 
        'training': ['14167534527_781ceb1b7a_n.jpg',...], 
        'testing': ['20773528301_008fcbc5a1_n.jpg',...],
        'validation': ['721595842_bacd80a6ac.jpg',...]
    }), 
    ...
])

```

---
##获取图片全路径的函数get_image_path

首先利用上面的create_image_lists方法生成图片列表，然后可以在下面函数中直接使用它。

get_image_path函数主要是从image_lists中恢复出某个图片路径。

增加和修改的代码
```
#所有图片列表对象
image_lists=create_image_lists()

#获取一个图片路径,label_name花类名同dir_name，category是training/testingvalidation,index是图片索引,set_dir可替换flower_photos文件夹名
def get_image_path(label_name,category,index,set_dir=image_dir): 
    label_lists = image_lists[dir_name]
    category_list = label_lists[category]        
    mod_index = index % len(category_list) #避免超出长度范围
    base_name = category_list[mod_index]
    sub_dir = label_lists['dir']
    full_path = os.path.join(image_dir, sub_dir, base_name)
    
    return full_path

#入口函数
def main(_):       
    get_image_path('daisy','training',66)
```

如果把上面返回的full_path打印出来，大概是
```
/Users/zhyuzh/desktop/.../flower_photos/daisy/267148092_4bb874af58.jpg

```

---
##生成瓶颈文件路径的函数get_bottleneck_path

Bottleneck瓶颈文件是对原始众多图片数据进行整理后的数据文件，能够更加方便的被tensorflow调用来训练、检验或预测使用。具体创建方法在下面会详解，这里只是先生成一个存放瓶颈文件的目录。

以下是修改和增加的代码
```
bottleneck_dir=os.path.join(dir_path,'bottlenecks')  

#获取一个瓶颈文件路径的函数
def get_bottleneck_path(label_name, category,index):
    module_name = (HUB_MODULE.replace('://', '~')  # URL scheme.
                   .replace('/', '~')  # URL and Unix paths.
                    .replace(':', '~').replace('\\', '~'))  # Windows paths.
    return get_image_path(label_name, category,index,bottleneck_dir) + '_' + 'module_name' + '.txt' #为了简化路径，我们临时使用字符串module_name而不是变量

#入口函数
def main(_):       
    bnpath=get_bottleneck_path('daisy','training',66)
    print(bnpath)
```
---
##从hub.ModuleSpec生成图和模型的函数create_module_graph

因为我们并不是完全从头开始训练模型，而是在hub的某个模型的基础上进行**再训练**，所以首先我们要从hub上拉取模型信息，并从中恢复出原计算图graph的一些张量参数以便于使用。

```
#要使用的hub模型
HUB_MODULE='https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/feature_vector/1'

#hub模型中要使用的量化操作节点名
FAKE_QUANT_OPS = ('FakeQuantWithMinMaxVars',
                  'FakeQuantWithMinMaxVarsPerChannel')

#创建从一个hub.ModuleSpec生成计算图并从Hub载入模型的函数
#module_spec需要使用的hub.ModuleSpec，bottleneck_tensor模型输出的额bottleneck_tensor值
#resized_input_tensor模型期望的输入的图像数据的尺寸，wants_quantization是否要量化
def create_module_graph(module_spec):
    height, width = hub.get_expected_image_size(module_spec)
    with tf.Graph().as_default() as graph:
        resized_input_tensor = tf.placeholder(tf.float32, [None, height, width, 3])
        m = hub.Module(module_spec)
        bottleneck_tensor = m(resized_input_tensor)
        wants_quantization = any(node.op in FAKE_QUANT_OPS
                                 for node in graph.as_graph_def().node) #any任何一个为真即为真
    return graph, bottleneck_tensor, resized_input_tensor, wants_quantization


#入口函数
def main(_):       
    module_spec = hub.load_module_spec(HUB_MODULE)
    result=create_module_graph(module_spec)
    print(result)
```

输出结果如下,包含了graph, bottleneck_tensor, resized_input_tensor, wants_quantization四个字段：
```
(
  <tensorflow.python.framework.ops.Graph object at 0x11b3da668>, 
  <tf.Tensor 'module_apply_default/hub_output/feature_vector/SpatialSqueeze:0'   shape=(?, 1280) dtype=float32>, 
  <tf.Tensor 'Placeholder:0' shape=(?, 224, 224, 3) dtype=float32>, 
  False
)
```

---
##提取图片瓶颈值的函数run_bottleneck_on_image

上面的代码我们从hub获得了模型，并提取到了graph计算图，这个函数将使用计算图中的两个张量进行运算，先对图片进行调整尺寸转为张量，然后提取它的瓶颈张量值。

以下是增加的代码，暂时不运行它，稍后和下面的函数一起测试：
```
#对一张图片执行推断，提取瓶颈总结层summary layer
#sess当前session，image_data字符串格式jpeg数据，image_data_tensor图的输入数据层
#decoded_image_tensor图像改变尺寸和处理后的输出，resized_input_tensor识别图的输入节点
#bottleneck_tesnor最终softmax之前的层
#返回瓶颈值数组numpy array
def run_bottleneck_on_image(sess, image_data, image_data_tensor,
                            decoded_image_tensor, resized_input_tensor,
                            bottleneck_tensor):
    resized_input_values = sess.run(decoded_image_tensor, #解码JPEG，调整大小，放缩像素值
                                    {image_data_tensor: image_data}) #feed_dict
    bottleneck_values = sess.run(bottleneck_tensor, #使用识别网络运行它
                                 {resized_input_tensor: resized_input_values}) #feed_dict
    bottleneck_values = np.squeeze(bottleneck_values) #去掉冗余的数组嵌套，简化形状
    return bottleneck_values
```
---
##创建瓶颈文件的函数create_bottleneck_file

首先我们创建ensure_dir_exists函数，确保文件夹存在，不存在的话就创建它。

然后在create_bottleneck_file函数中我们先用上面创建的get_bottleneck_path方法获取存储文件路径bottleneck_path，同样获取图片路径image_path并读取图片数据image_data，使用上面创建的run_bottleneck_on_image函数把图片数据利用session和graph内的张量，转为瓶颈值并保存到文件中。

以下是新增代码，仍然不能运行，因为参数jpeg_data_tensor, decoded_image_tensor还无法获得，稍后我们会一起测试：
```
#确保目录路径存在，不存在就创建
def ensure_dir_exists(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

#创建一个瓶颈文件
def create_bottleneck_file(sess,label_name,category, index, jpeg_data_tensor,
                           decoded_image_tensor, resized_input_tensor,
                           bottleneck_tensor):
    sub_dir=os.path.join(dir_path,'bottlenecks/'+label_name)  
    ensure_dir_exists(sub_dir) #创建文件夹
    
    bottleneck_path=get_bottleneck_path(label_name, category,index) #存储瓶颈文件的路径
    tf.logging.info('正在创建bottleneck文件：' + bottleneck_path)
    image_path = get_image_path(label_name,category,index) #获取图片文件全路径
    image_data = tf.gfile.FastGFile(image_path, 'rb').read() #获取文件原数据
    try:
        bottleneck_values = run_bottleneck_on_image( #从图片生成瓶颈值
            sess,image_data, jpeg_data_tensor, decoded_image_tensor,
            resized_input_tensor, bottleneck_tensor)
    except Exception as e:
        raise RuntimeError('处理文件出错 %s (%s)' % (image_path,str(e)))
    bottleneck_string = ','.join(str(x) for x in bottleneck_values)
    with open(bottleneck_path, 'w') as bottleneck_file:
        bottleneck_file.write(bottleneck_string) #将获得的bottleneck值用逗号连接成字符串写入文件
```

---
##向计算图添加图片解码操作的函数add_jpeg_decoding

jpg_data_tensor是一个placeholder，decoded_image_tensor是调整过大小的图像数据张量格式。

下面是新增和修改的代码，可以结合上面两个函数一起测试运行：
```
#添加操作，执行jpeg解码和调整大小 ，返回两个张量jpeg_data_tensor,decoded_image_tensor    
def add_jpeg_decoding(module_spec):
    input_height, input_width = hub.get_expected_image_size(module_spec)
    input_depth = hub.get_num_image_channels(module_spec)
    jpeg_data = tf.placeholder(tf.string, name='DecodeJPGInput')
    decoded_image = tf.image.decode_jpeg(jpeg_data, channels=input_depth)
    #将全范围的unit8转为0~1范围的float32
    decoded_image_as_float = tf.image.convert_image_dtype(decoded_image,tf.float32)
    decoded_image_4d = tf.expand_dims(decoded_image_as_float, 0) #扩充形状的维度
    resize_shape = tf.stack([input_height, input_width]) #通过合并提升维度
    resize_shape_as_int = tf.cast(resize_shape, dtype=tf.int32)
    resized_image = tf.image.resize_bilinear(decoded_image_4d,
                                             resize_shape_as_int)  #放缩图像尺寸
    return jpeg_data, resized_image


#入口函数
def main(_):
    module_spec = hub.load_module_spec(HUB_MODULE)
    graph, bottleneck_tensor, resized_input_tensor, wants_quantization = (
        create_module_graph(module_spec))
    
    with tf.Session(graph=graph) as sess:
        init = tf.global_variables_initializer()
        sess.run(init)

        jpeg_data_tensor, decoded_image_tensor = add_jpeg_decoding(module_spec)
        create_bottleneck_file(sess,'daisy','training', 65, jpeg_data_tensor,
                               decoded_image_tensor, resized_input_tensor,
                               bottleneck_tensor)
```
在main函数里面我们先是利用hub.load_module_spec载入了模型，然后使用create_module_graph创建了图，已经从图中提取的bottleneck_tensor和resized_inpt_tensor。

然后我们利用graph创建了session，初始化了变量，又使用add_jpeg_decoding方法创建了两个张量jpeg_data_tensor和decoded_image_tensor。

最后我们使用create_bottleneck_file方法，在/bottlenecks/daisy/目录下创建了一个文件，并把我们得到的图片bottleneck数据写入其中。

这个文件的都是很多的浮点小数，这些数字在另外的角度上反映了像素之间的关系，而tensorflow能够从中更加容易的找到规律:
```python
1.1014792,1.7321489,0.284751,0.7904396,0.0,0.11441692,0.0,0.30288044,0.07657591,0.353643,0.0,1.2191151,0.3042915,1.0002377,0.18627474,0.4791365,0.0,0.058162533,1.0755428,0.047679365,0.0,1.5222605,0.51027495,0.109168105,0.3694405,0.014923426,0.0032605443,2.3457944,0.5158326...
```

---
##阶段小结

这阶段我们主要编写了几个函数，实现了图像文件的列表生成、bottleneck文件的创建的内容：

1. 读取图片列表create_image_lists
1. 获取图片全路径的函数get_image_path
1. 生成瓶颈文件路径的函数get_bottleneck_path
1. 从hub.ModuleSpec生成图和模型的函数create_module_graph
1. 提取图片瓶颈值的函数run_bottleneck_on_image
1. 确保路径文件夹存在的函数ensure_dir_exists
1. 创建瓶颈文件的函数create_bottleneck_file
1. 向计算图添加图片解码操作的函数add_jpeg_decoding

以下是此阶段的全部代码：
```
import argparse
import collections
from datetime import datetime
import hashlib
import random
import re
import sys

import os
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

dir_path = os.path.dirname(os.path.realpath(__file__))
image_dir=os.path.join(dir_path,'flower_photos')  
bottleneck_dir=os.path.join(dir_path,'bottlenecks')  

MAX_IPC = 2 ** 27 - 1 #每分类最大图片数max-image-per-class

#要使用的hub模型，就是module_name
HUB_MODULE='https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/feature_vector/1'

#hub模型中要使用的量化操作节点名
FAKE_QUANT_OPS = ('FakeQuantWithMinMaxVars',
                  'FakeQuantWithMinMaxVarsPerChannel')


#获取全部文件列表
def create_image_lists(): 
  
    result = collections.OrderedDict() #有序字典，匹配顺序到labels
    sub_dirs = sorted(x[0] for x in tf.gfile.Walk(image_dir)) #获得花类型文件夹列表，第一个是根目录
    
    
    is_root_dir = True
    for sub_dir in sub_dirs:        
        if is_root_dir: #跳过根目录
            is_root_dir = False
            continue
            
        extensions = ['jpg', 'jpeg', 'JPG', 'JPEG']
        file_list = []
        dir_name = os.path.basename(sub_dir) #得到花分类的名字daisy，rose...
        if dir_name == image_dir:
            continue
        for extension in extensions:
            file_glob = os.path.join(image_dir, dir_name, '*.' + extension) #获取所有图片路径
            file_list.extend(tf.gfile.Glob(file_glob)) #将所有图片路径加入到file_list  
        label_name = re.sub(r'[^a-z0-9]+', ' ', dir_name.lower()) #清理花分类名称字符，这里没意义
        
        training_images = [] #用于训练的图片路径
        testing_images = [] #用于测试的图片路径
        validation_images = [] #用于验证的图片路径
        for file_name in file_list:
            base_name = os.path.basename(file_name) #得到文件名7166550328_de0d73cfa9.jpg...
            hash_name = re.sub(r'_nohash_.*$', '', file_name) #得到图片全路径
            hash_name_hashed = hashlib.sha1(tf.compat.as_bytes(hash_name)).hexdigest() #转40位hash
            hash_int=int(hash_name_hashed, 16) #转超长的整数
            hash_per=hash_int%(MAX_IPC + 1)*(100.0 / MAX_IPC) #放缩到0~100

            if hash_per < 10: #验证集10%
                validation_images.append(base_name)
            elif hash_per < 30: #测试集20%
                testing_images.append(base_name)
            else: #训练集70%
                training_images.append(base_name)
                
        result[label_name] = {
            'dir': dir_name,
            'training': training_images,
            'testing': testing_images,
            'validation': validation_images,
        }
    return result

#所有图片列表对象
image_lists=create_image_lists()

#获取一个图片路径,label_name花类名同dir_name，category是training/testingvalidation,index是图片索引,set_dir可替换flower_photos文件夹名
def get_image_path(label_name,category,index,set_dir=image_dir): 
    label_lists = image_lists[label_name]
    category_list = label_lists[category]        
    mod_index = index % len(category_list) #避免超出长度范围
    base_name = category_list[mod_index]
    sub_dir = label_lists['dir']
    full_path = os.path.join(set_dir, sub_dir, base_name)
    
    return full_path

#获取一个瓶颈文件路径的函数
def get_bottleneck_path(label_name, category,index):
    module_name = (HUB_MODULE.replace('://', '~')  # URL scheme.
                   .replace('/', '~')  # URL and Unix paths.
                    .replace(':', '~').replace('\\', '~'))  # Windows paths.
    return get_image_path(label_name, category,index,bottleneck_dir) + '_' + 'module_name' + '.txt'

#创建从一个hub.ModuleSpec生成计算图并从Hub载入模型的函数
#module_spec需要使用的hub.ModuleSpec，bottleneck_tensor模型输出的额bottleneck_tensor值
#resized_input_tensor模型期望的输入的图像数据的尺寸，wants_quantization是否要量化
def create_module_graph(module_spec):
    height, width = hub.get_expected_image_size(module_spec)
    with tf.Graph().as_default() as graph:
        resized_input_tensor = tf.placeholder(tf.float32, [None, height, width, 3])
        m = hub.Module(module_spec)
        bottleneck_tensor = m(resized_input_tensor)
        wants_quantization = any(node.op in FAKE_QUANT_OPS
                                 for node in graph.as_graph_def().node) #any任何一个为真即为真
    return graph, bottleneck_tensor, resized_input_tensor, wants_quantization


#对一张图片执行推断，提取瓶颈总结层summary layer
#sess当前session，image_data字符串格式jpeg数据，image_data_tensor图的输入数据层
#decoded_image_tensor图像改变尺寸和处理后的输出，resized_input_tensor识别图的输入节点
#bottleneck_tesnor最终softmax之前的层
#返回瓶颈值数组numpy array
def run_bottleneck_on_image(sess,image_data, image_data_tensor,
                            decoded_image_tensor, resized_input_tensor,
                            bottleneck_tensor):
    resized_input_values = sess.run(decoded_image_tensor, #解码JPEG，调整大小，放缩像素值
                                    {image_data_tensor: image_data}) #feed_dict
    bottleneck_values = sess.run(bottleneck_tensor, #使用识别网络运行它
                                 {resized_input_tensor: resized_input_values}) #feed_dict
    bottleneck_values = np.squeeze(bottleneck_values) #去掉冗余的数组嵌套，简化形状
    return bottleneck_values


#确保目录路径存在，不存在就创建
def ensure_dir_exists(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

#创建一个瓶颈文件
def create_bottleneck_file(sess,label_name,category, index, jpeg_data_tensor,
                           decoded_image_tensor, resized_input_tensor,
                           bottleneck_tensor):
    sub_dir=os.path.join(dir_path,'bottlenecks/'+label_name)  
    ensure_dir_exists(sub_dir) #创建文件夹
    
    bottleneck_path=get_bottleneck_path(label_name, category,index) #存储瓶颈文件的路径
    tf.logging.info('正在创建bottleneck文件：' + bottleneck_path)
    image_path = get_image_path(label_name,category,index) #获取图片文件全路径
    image_data = tf.gfile.FastGFile(image_path, 'rb').read() #获取文件原数据
    try:
        bottleneck_values = run_bottleneck_on_image( #从图片生成瓶颈值
            sess,image_data, jpeg_data_tensor, decoded_image_tensor,
            resized_input_tensor, bottleneck_tensor)
    except Exception as e:
        raise RuntimeError('处理文件出错 %s (%s)' % (image_path,str(e)))
    bottleneck_string = ','.join(str(x) for x in bottleneck_values)
    with open(bottleneck_path, 'w') as bottleneck_file:
        bottleneck_file.write(bottleneck_string) #将获得的bottleneck值用逗号连接成字符串写入文件
        
#添加操作，执行jpeg解码和调整大小 ，返回两个张量jpeg_data_tensor,decoded_image_tensor    
def add_jpeg_decoding(module_spec):
    input_height, input_width = hub.get_expected_image_size(module_spec)
    input_depth = hub.get_num_image_channels(module_spec)
    jpeg_data = tf.placeholder(tf.string, name='DecodeJPGInput')
    decoded_image = tf.image.decode_jpeg(jpeg_data, channels=input_depth)
    #将全范围的unit8转为0~1范围的float32
    decoded_image_as_float = tf.image.convert_image_dtype(decoded_image,tf.float32)
    decoded_image_4d = tf.expand_dims(decoded_image_as_float, 0) #扩充形状的维度
    resize_shape = tf.stack([input_height, input_width])
    resize_shape_as_int = tf.cast(resize_shape, dtype=tf.int32)
    resized_image = tf.image.resize_bilinear(decoded_image_4d,
                                             resize_shape_as_int)
    return jpeg_data, resized_image


#入口函数
def main(_):
    module_spec = hub.load_module_spec(HUB_MODULE)
    graph, bottleneck_tensor, resized_input_tensor, wants_quantization = (
        create_module_graph(module_spec))
    
    with tf.Session(graph=graph) as sess:
        init = tf.global_variables_initializer()
        sess.run(init)

        jpeg_data_tensor, decoded_image_tensor = add_jpeg_decoding(module_spec)
        create_bottleneck_file(sess,'daisy','training', 65, jpeg_data_tensor,
                               decoded_image_tensor, resized_input_tensor,
                               bottleneck_tensor)   
    

#模块或应用
if __name__ == '__main__':
    tf.app.run()
```

---
###探索人工智能的新边界
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，感谢转发~
---
END