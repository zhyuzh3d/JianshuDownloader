人类大脑可以轻而易举的识别图像中的狮子和豹子，识别各种符号和文字，识别人脸，等等，但这些对于计算机来说就很难。因为我们的大脑尤其擅长图像识别。

>题外，其实也并非完全如此，对于陌生的内容，我们并不能做的太好，比如你可能看过太多的日文字幕，但再看到屏幕上的日文符号的时候，你还记得它是否在《名侦探柯南》中出现过吗？同样，我们对于华人明星的脸几乎从不会搞混谁是谁，但对于欧美明不太知名的明星恐怕就经常分不清哪个是哪个。人类也经常被各种视觉错觉所欺骗，比如经常去看的3D电影，一块幕布竟然被我们看出了立体感，不觉得奇怪吗？这里面一定隐藏着什么一些未被重视的算法。

在过去的几年，计算机科学家在图像识别上取得了重大突破，尤其是CNN卷积神经网络的使用，计算机已经能够解决很多有难度的图像识别任务，甚至某些领域比人做的还好。

计算机视觉算法已经攻克了学院派的ImageNet测试标准，成功的模型不断进步： [QuocNet](https://static.googleusercontent.com/media/research.google.com/en//archive/unsupervised_icml2012.pdf), [AlexNet](https://www.cs.toronto.edu/~fritz/absps/imagenet.pdf), [Inception (GoogLeNet)](https://arxiv.org/abs/1409.4842), [BN-Inception-v2](https://arxiv.org/abs/1502.03167)，Google谷歌内部和外部的科学家正在探讨下一代图像识别模型，[Inception-v3](https://arxiv.org/abs/1512.00567)。

Inception-v3是基于2012年以来ImageNet图片挑战赛数据训练得到的，这个挑战赛是计算机视觉的标杆性的比赛，需要识别1000种分类，比如斑马、斑点狗和洗碗机等，比如下面是AlexNet模型识别的一些分类：
![螨虫，货船，踏板摩托，美洲豹；粉色条表示了最大可能的分类，都获得了正确的结果](imgs/4324074-eead8898a5eda8c9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

为了对比模型，我们检查模型预测失败率最高的5个预测，AlexNet在2012年top5错误率是15.3%,Inception是6.67%，Inception-v2是4.9，Inception-v3是3.46%。而人类的top-5错误率是5.1%。

本篇教程将介绍如何使用Inception-v3识别1000种分类，也会介绍如何从这个模型种提取更高特征，以便于用其他识别任务。

---
##准备工作

首先从[百度云盘下载相关文件](https://pan.baidu.com/s/1tDd0aSJaJx5ToV_wpzO2bg)(密码:fxrs)

其中包含了saved_model和imgs两个文件夹
* **saved_model**，这里是谷歌Inception项目基于众多图片训练好的模型，以及分类名称对照表数据(label_map_proto.pbtxt，nameid2name.txt)。这里是已保存的模型，而不是checkpoint文件。
* **imgs**,只是一张将被识别的熊猫图片。

>这次我将tensorflow升级到了1.7，推荐通过下面命令行升级
```
pip3 install --upgrade pip
pip3 install --upgrade tensorflow
```

---
##代码结构

```
import os
import re #regular expressions正则表达式操作模块
import numpy as np
import tensorflow as tf

#准备目录
dir_path = os.path.dirname(os.path.realpath(__file__))
model_dir=os.path.join(dir_path,'saved_model')  
image_path=os.path.join(dir_path, 'imgs/panda.jpg')
proto_path=os.path.join(dir_path, 'saved_model/label_map_proto.pbtxt')
name_path=os.path.join(dir_path, 'saved_model/nameid2name.txt')
model_path=os.path.join(model_dir, 'classify_image_graph_def.pb')

#我们的主要代码将添加在这里

#入口函数
def main(_):    
    #在这里运行测试


#模块或应用
if __name__ == '__main__':
    tf.app.run()
```

---
##加载分类名称对照表函数

首先看一下两个文件的内容：

分类类别编号（target_class即nodeid）和名称编号（ target_class_string即nameid）的对应关系label_map_proto.pbtxt:
```python
# -*- protobuffer -*-
# LabelMap from ImageNet 2012 full data set UID to int32 target class.
entry {
  target_class: 449
  target_class_string: "n01440764"
}
entry {
  target_class: 450
  target_class_string: "n01443537"
}
```
名称编号（n开头）和名称的对应关系nameid2name.txt:
```
n00004475	organism, being
n00005787	benthos
n00006024	heterotroph
n00006484	cell
n00007846	person, individual, someone, somebody, mortal, soul
```

我们向代码添加获取分类的函数get_class,并喂它创建两个方法：
* **load**，用来读取两个文件，逐行读取，然后拆分，重组成为两个字典{nodeid:nameid}和{nameid:name}，再把两个字典合并成为{nodeid:name}
* **get_name_by_nodeid**,根据上面的字典，通过nodeid获取name。
并在__init__里面自动使用load()方法读取。

在main里面运行并测试,增加和修改的部分代码如下:
```
#用来把分类节点nodeid转为物体名称字符串的函数
class get_class():
    def __init__(self):
        self.class_list=self.load() #载入，生成{nodeid:name}字典
       
    #从文本载入名称id映射数据
    def load(self):
        #读取nameid和name的对应关系
        nameid2name = {} #字典{nid:name}
        lines1 = tf.gfile.GFile(name_path).readlines()
        p = re.compile(r'[n\d]*[ \S,]*') #定义正则匹配方式
        for line in lines1:
            #findall将n00004475	organism, being分解成['n00004475','organism, being']
            parsed_items = p.findall(line) 
            nid = parsed_items[0]
            name = parsed_items[2]
            nameid2name[nid] = name
            
        #读取nodeid和nameid的对应关系  
        nodeid2nameid = {}
        lines2 = tf.gfile.GFile(proto_path).readlines()
        for line in lines2:
            #参考数据格式entry {
            #  target_class: 449
            #  target_class_string: "n01440764"
            #}
            if line.startswith('  target_class:'):
                target_class = int(line.split(': ')[1])
            if line.startswith('  target_class_string:'):
                target_class_string = line.split(': ')[1]
                nodeid2nameid[target_class] = target_class_string[1:-2]
                
        #合并成nodeid和name的对应关系
        nodeid2name = {}
        for key, val in nodeid2nameid.items():
            if val not in nameid2name:
                tf.logging.fatal('对应失败: %s', val)
            name = nameid2name[val]
            nodeid2name[key] = name
                
        print(nodeid2name) #这里打印结果！
        return nodeid2name
    
    #根据nodeid获取分类名
    def get_name_by_nodeid(self, nodeid):
        if nodeid not in self.class_list:
            return ''
        return self.class_list[nodeid]                

#入口函数
def main(_):    
    getclass = get_class()
```
运行将会打印出结果,编号对应了名称。
```
{449: 'tench, Tinca tinca', 450: 'goldfish, Carassius auratus', 442: 'great white shark, white shark, man-eater, man-eating shark, Carcharodon carcharias', 443: 'tiger shark,...
```
>这个操作其实没什么意义，但是如果没有这个450到'goldfish, Carassius auratus'（金鱼）的转换，那么稍后预测出我们的图片是565，我们也没法知道这是什么鬼。

---
##读取已保存的模型

我们使用```tf.gfile```来读取保存的pd文件```model_path=os.path.join(model_dir, 'classify_image_graph_def.pb')```,把内容恢复到```tf.GraphDef```tensorflow的计算图中。

下面是增加和修改部分的代码，运行后没有输出结果。
```
#从保存的模型读取graph
def create_graph():
    with tf.gfile.FastGFile(model_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

 #入口函数
def main(_):    
    create_graph()
```


---
##对图片进行预测的函数

签名create_graph载入已保存模型创建了图，我们只要从graph中找出最终输出的张量softmax，然后利用feed_dict重新喂食我们的图片，就能run出预测结果。
当然别忘了用我们辛苦编写的get_class来把预测的nodeid改为可以读懂的名称再打印出来。

增加和修改部分的代码如下：
```
#执行预测
def predict_image():
    image_data = tf.gfile.FastGFile(image_path, 'rb').read() #读取图片
    create_graph() #创建计算图

    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('softmax:0') #从计算图中提取张量
        predictions = sess.run(softmax_tensor,{'DecodeJpeg/contents:0': image_data}) #输入feed_dict进行运算
        predictions = np.squeeze(predictions) #去掉冗余的1维形状，比如把张量形状从(1,3,1)变为(3)

        #输出打印
        getclass = get_class()
        top5 = predictions.argsort()[-5:][::-1]
        
        print('\n预测结果是：')
        for node_id in top5:
            name_string = getclass.get_name_by_nodeid(node_id)
            score = predictions[node_id]
            print('%s (score = %.5f)' % (name_string, score))
        

#入口函数
def main(_):    
    predict_image()
```

这次运行就能预测大熊猫(giant panda)了！输出类似下面的结果,0.89107表示这个图片有89.107%的可能是大熊猫：
```
预测结果是：
giant panda, panda, panda bear, coon bear, Ailuropoda  (score = 0.89107)
indri, indris, Indri indri, Indri brevicaudatus (score = 0.00779)
lesser panda, red panda, panda, bear cat, cat bear, Ailurus fulgens (score = 0.00296)
custard apple (score = 0.00147)
earthstar (score = 0.00117)
```

---
##结语

使用谷歌Inception项目训练好的模型来预测图片，其实关键代码很简单，就是载入模型，重新生成计算图，进行预测。但大篇幅的代码都是get_class来转换文字的。
下面是全部代码：
```
import os
import re #regular expressions正则表达式操作模块
import numpy as np
import tensorflow as tf

#准备目录
dir_path = os.path.dirname(os.path.realpath(__file__))
model_dir=os.path.join(dir_path,'saved_model')  
image_path=os.path.join(dir_path, 'imgs/panda.jpg')
proto_path=os.path.join(dir_path, 'saved_model/label_map_proto.pbtxt')
name_path=os.path.join(dir_path, 'saved_model/nameid2name.txt')
model_path=os.path.join(model_dir, 'classify_image_graph_def.pb')

#用来把分类节点nodeid转为物体名称字符串的函数
class get_class():
    def __init__(self):
        self.class_list=self.load() #载入，生成{nodeid:name}字典
       
    #从文本载入名称id映射数据
    def load(self):
        #读取nameid和name的对应关系
        nameid2name = {} #字典{nid:name}
        lines1 = tf.gfile.GFile(name_path).readlines()
        p = re.compile(r'[n\d]*[ \S,]*') #定义正则匹配方式
        for line in lines1:
            #findall将n00004475	organism, being分解成['n00004475','organism, being']
            parsed_items = p.findall(line) 
            nid = parsed_items[0]
            name = parsed_items[2]
            nameid2name[nid] = name
            
        #读取nodeid和nameid的对应关系  
        nodeid2nameid = {}
        lines2 = tf.gfile.GFile(proto_path).readlines()
        for line in lines2:
            #参考数据格式entry {
            #  target_class: 449
            #  target_class_string: "n01440764"
            #}
            if line.startswith('  target_class:'):
                target_class = int(line.split(': ')[1])
            if line.startswith('  target_class_string:'):
                target_class_string = line.split(': ')[1]
                nodeid2nameid[target_class] = target_class_string[1:-2]
                
        #合并成nodeid和name的对应关系
        nodeid2name = {}
        for key, val in nodeid2nameid.items():
            if val not in nameid2name:
                tf.logging.fatal('对应失败: %s', val)
            name = nameid2name[val]
            nodeid2name[key] = name
                
        return nodeid2name
    
    #根据nodeid获取分类名
    def get_name_by_nodeid(self, nodeid):
        if nodeid not in self.class_list:
            return ''
        return self.class_list[nodeid]                

#从保存的模型读取graph
def create_graph():
    with tf.gfile.FastGFile(model_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')
        
#执行预测
def predict_image():
    image_data = tf.gfile.FastGFile(image_path, 'rb').read() #读取图片
    create_graph() #创建计算图

    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('softmax:0') #从计算图中提取张量
        predictions = sess.run(softmax_tensor,{'DecodeJpeg/contents:0': image_data}) #输入feed_dict进行运算
        predictions = np.squeeze(predictions) #去掉冗余的1维形状，比如把张量形状从(1,3,1)变为(3)

        #输出打印
        getclass = get_class()
        top5 = predictions.argsort()[-5:][::-1]
        
        print('\n预测结果是：')
        for node_id in top5:
            name_string = getclass.get_name_by_nodeid(node_id)
            score = predictions[node_id]
            print('%s (score = %.5f)' % (name_string, score))
        
#入口函数
def main(_):    
    predict_image()

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










