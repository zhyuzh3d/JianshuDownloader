我们[继续前一篇文章](https://www.jianshu.com/p/2c83da04562f)，来逐步完成图像再训练的整个案例。

在上一篇我们实现了bottleneck文件的创建，如果文件已经创建了，那么我们可以直接使用，否则我们就创建它，我们继续...

---
##取得或创建瓶颈文件的函数get_or_create_bottleneck

这个函数其实只是读取存储的bottleneck文件数据，如果没有的话就立即创建。

下面是新增和修改的代码，可结合上一篇的代码运行测试：
```
#取得或创建瓶颈文件数据，如果没有就创建它。返回由bottleneck层产生的图片的numpy array数组
def get_or_create_bottleneck(sess, label_name, category, index, jpeg_data_tensor,
                             decoded_image_tensor, resized_input_tensor,
                             bottleneck_tensor):
    label_lists = image_lists[label_name]
    sub_dir = label_lists['dir'] #获取花分类名如'daisy'
    sub_dir_path = os.path.join(bottleneck_dir, sub_dir)
    ensure_dir_exists(sub_dir_path) #确保路径文件夹存在    
    bottleneck_path = get_bottleneck_path(label_name, category,index)
    
    if not os.path.exists(bottleneck_path): #如果文件不存在就创建文件
        create_bottleneck_file(sess, label_name, category,index,jpeg_data_tensor,
                               decoded_image_tensor, resized_input_tensor,
                               bottleneck_tensor)    
    
    with open(bottleneck_path, 'r') as bottleneck_file: #读取瓶颈文件
        bottleneck_string = bottleneck_file.read()
    
    did_hit_error = False #遇到错误
    try:
        bottleneck_values = [float(x) for x in bottleneck_string.split(',')]
    except ValueError:
        tf.logging.warning('在重建瓶颈文件时遇到非法浮点数')
        did_hit_error = True    
    
    if did_hit_error: #如果出错就重建瓶颈文件
        create_bottleneck_file(sess, label_name, category,index,jpeg_data_tensor,
                               decoded_image_tensor, resized_input_tensor,
                               bottleneck_tensor)        
        with open(bottleneck_path, 'r') as bottleneck_file:
            bottleneck_string = bottleneck_file.read() 
        bottleneck_values = [float(x) for x in bottleneck_string.split(',')]
        
    return bottleneck_values

#入口函数
def main(_):
    module_spec = hub.load_module_spec(HUB_MODULE)
    graph, bottleneck_tensor, resized_input_tensor, wants_quantization = (
        create_module_graph(module_spec))
    
    with tf.Session(graph=graph) as sess:
        init = tf.global_variables_initializer()
        sess.run(init)

        jpeg_data_tensor, decoded_image_tensor = add_jpeg_decoding(module_spec)
        get_or_create_bottleneck(sess,'daisy','training', 65, jpeg_data_tensor,
                               decoded_image_tensor, resized_input_tensor,
                               bottleneck_tensor)
```
如果我们打印bottleneck_values就会得到一长串数字组成的数组。
```
[0.070175596, 0.2166954, 0.0072527127, 0.04728513, 1.1940469, 0.7925658, 2.029932, ...]
```

---
##确保瓶颈文件都被缓存的函数cache_bottlenecks

因为在训练过程中，对同一个图片会反复多次读取(不对图像进行扭曲处理的话)，如果我们对图片bottleneck缓存就能大大提高效率。

我们将用这个函数检查所有图片进行计算并保存。这个函数其实也只是循环调用前面的get_or_create_bottleneck函数。

下面是增加和修改的代码，可以运行测试：
```
#确保所有的training、testing、validation要用的bottleneck文件都已经被缓存
def cache_bottlenecks(sess,jpeg_data_tensor, decoded_image_tensor,
                      resized_input_tensor, bottleneck_tensor):
    how_many_bottlenecks = 0
    ensure_dir_exists(bottleneck_dir)
    for label_name, label_lists in image_lists.items():
        for category in ['training', 'testing', 'validation']:
            category_list = label_lists[category] #针对每一个分类，比如daisy
            for index, unused_base_name in enumerate(category_list): #创建索引
                get_or_create_bottleneck(
                    sess, label_name, category,index,
                    jpeg_data_tensor, decoded_image_tensor,
                    resized_input_tensor, bottleneck_tensor)

                how_many_bottlenecks += 1
                if how_many_bottlenecks % 100 == 0:
                    tf.logging.info(str(how_many_bottlenecks) + '瓶颈文件被创建.') #每100张输出一次提示

#入口函数
def main(_):
    tf.logging.set_verbosity(tf.logging.INFO)
    module_spec = hub.load_module_spec(HUB_MODULE)
    graph, bottleneck_tensor, resized_input_tensor, wants_quantization = (
        create_module_graph(module_spec))
    
    with tf.Session(graph=graph) as sess:
        init = tf.global_variables_initializer()
        sess.run(init)
        jpeg_data_tensor, decoded_image_tensor = add_jpeg_decoding(module_spec)
        
        cache_bottlenecks(sess, jpeg_data_tensor,decoded_image_tensor, 
                          resized_input_tensor,bottleneck_tensor)
```
运行过程中会隔一会（处理100张）输出一行提示。整个过程可能需要十几分钟或更久，全部完成后会在/bottlenecks/文件夹下增加每个花类别的文件夹并且里面包含了很多很多txt文件。

---
##随机获取一批bottleneck文件数据get_random_cached_bottlenecks

从所有的分类图片中随机选取一些bottleneck数据，主要是使用了get_or_create_bottleneck函数。

以下是新增和修改的代码，可以结合前面的代码运行测试：
```
#随机获取所有种类中随机bottleneck数据列表、对应的label_index和图片文件路径列表,
#how_many数量小于等于0时候获取全部
def get_random_cached_bottlenecks(sess, how_many, category, 
                                  jpeg_data_tensor,decoded_image_tensor,
                                  resized_input_tensor,bottleneck_tensor):
    class_count = len(image_lists.keys()) #有多少种花分类
    bottlenecks = []
    ground_truths = [] #label_index花分类索引号
    filenames = [] #图片文件路径列表
    
    if how_many >= 0:
        for unused_i in range(how_many):
            label_index = random.randrange(class_count) #随机一种花如daisy
            label_name = list(image_lists.keys())[label_index] #daisy
            image_index = random.randrange(MAX_IPC + 1) #每种类最大数量，如果超过后面会自动取余数
            image_name = get_image_path(label_name,category,image_index) #图片路径
            bottleneck = get_or_create_bottleneck( #读取bottleneck文件数据
              sess,  label_name, category, image_index,
              jpeg_data_tensor, decoded_image_tensor,
              resized_input_tensor, bottleneck_tensor)
            bottlenecks.append(bottleneck)
            ground_truths.append(label_index)
            filenames.append(image_name)
    else:
        for label_index, label_name in enumerate(image_lists.keys()):
            for image_index, image_name in enumerate(image_lists[label_name][category]): #建立某分类下图片索引
                image_name = get_image_path(label_name, category,image_index)
                bottleneck = get_or_create_bottleneck(
                    sess, label_name, category,image_index,  
                    jpeg_data_tensor, decoded_image_tensor,
                    resized_input_tensor, bottleneck_tensor)
                bottlenecks.append(bottleneck)
                ground_truths.append(label_index)
                filenames.append(image_name)
    
    return bottlenecks, ground_truths, filenames                   
                    
#入口函数
def main(_):
    tf.logging.set_verbosity(tf.logging.WARN)
    module_spec = hub.load_module_spec(HUB_MODULE)
    graph, bottleneck_tensor, resized_input_tensor, wants_quantization = (
        create_module_graph(module_spec))
    
    with tf.Session(graph=graph) as sess:
        init = tf.global_variables_initializer()
        sess.run(init)
        jpeg_data_tensor, decoded_image_tensor = add_jpeg_decoding(module_spec)
        
        result=get_random_cached_bottlenecks(sess, 5, 'training',
                                      jpeg_data_tensor,decoded_image_tensor,
                                      resized_input_tensor,bottleneck_tensor)
```
打印出result结果类似:
```python
(
    [[0.0, 1.8930491, 0.0, 0.0,... 0.1771909, 0.045966692],...x5],#5个bottleneck数据
    [0, 3, 3, 0, 2], #对应的5个标签编号
    ['/Users/zhyuzh/desktop/MyProjects/.../flower_photos/daisy/16161045294_70c76ce846_n.jpg', ...x5] #对应的5张图片路径
)
```

---
##随机获取变形的瓶颈数据get_random_distorted_bottlenecks

如果我们使用变形的图片进行训练，比如裁剪、放缩、翻转的图片，我们需要针对每个图片重新计算整个模型，所以我们不能使用原来缓存的图片bottleneck数据，我们需要使用另外的变形计算图来运行得到新的变形bottleneck数据，然后再把它投入到整个计算图进行训练。

首先我们回顾run_bottleneck_on_image函数:
```
def run_bottleneck_on_image(sess,image_data, image_data_tensor,
                            decoded_image_tensor, resized_input_tensor,
                            bottleneck_tensor):
    resized_input_values = sess.run(decoded_image_tensor, #解码JPEG，调整大小，放缩像素值
                                    {image_data_tensor: image_data}) #feed_dict
    bottleneck_values = sess.run(bottleneck_tensor, #使用识别网络运行它
                                 {resized_input_tensor: resized_input_values}) #feed_dict
    bottleneck_values = np.squeeze(bottleneck_values) #去掉冗余的数组嵌套，简化形状
    return bottleneck_values
```
这里我们看到参数传递进来的image_data图像数据，然后被喂食feed_dict到graph的decoded_image_tensor子图中运行得到resized_input_values。
然后再把结果喂食到graph的子图bottleneck_tensor中得到进一步结果。

这里需要新增的get_random_distorted_bottlenecks方法不使用现成的图像数据参数，而是从随机文件中读取，然后使用distorted_image子图对图像进行处理，然后同样将结果喂食到子图distorted_image_tensor中，得到进一步结果。

整体上这两个函数的实现思路是一样的。下面是新增的代码，请勿运行，稍后和后面的函数一起测试：
```
#随机获取变形的瓶颈数据，返回bottlenecks数组和对应的label_index数组
def get_random_distorted_bottlenecks(sess, how_many, category,
                                     input_jpeg_tensor,distorted_image_tensor, 
                                     resized_input_tensor, bottleneck_tensor):
    class_count = len(image_lists.keys()) #有几种花分类
    bottlenecks = [] #变形后的瓶颈数据
    ground_truths = [] #label_index标签编号
    for unused_i in range(how_many):
        label_index = random.randrange(class_count) #随机一个花分类
        label_name = list(image_lists.keys())[label_index] #daisy
        image_index = random.randrange(MAX_IPC + 1) #随机一张图
        image_path = get_image_path(label_name, category,image_index)
        
        if not tf.gfile.Exists(image_path):
            tf.logging.fatal('文件不存在 %s', image_path)
            
        #下面两句可以参考run_bottleneck_on_image函数
        jpeg_data = tf.gfile.FastGFile(image_path, 'rb').read()  #没有参数传递jpeg_data进来，要重新读取文件       
        distorted_image_data = sess.run(distorted_image_tensor,
                                        {input_jpeg_tensor: jpeg_data}) #feed_dict
        bottleneck_values = sess.run(bottleneck_tensor,
                                     {resized_input_tensor: distorted_image_data}) #feed_dict
        bottleneck_values = np.squeeze(bottleneck_values)
        bottlenecks.append(bottleneck_values)
        ground_truths.append(label_index)
        
    return bottlenecks, ground_truths
```


---
##生成变形图片操作ops的函数add_input_distortions

在训练的过程中我们对图片进行一些变形（裁切、放缩、翻转或调整亮度），可以利用有限数量的图片模拟更多的真实情况，进而有效改进模型。

这个函数里我们构建了新的graph用来对图片数据新建调整变换：
```
#生成两个变形操作ops的函数input_jpeg_tensor,distorted_image_tensor
#注意，只是生成一个grah并返回需要运行这个graph的两个feed_dict入口
def add_input_distortions(module_spec,flip_left_right, 
                          random_crop, random_scale,random_brightness):
    input_height, input_width = hub.get_expected_image_size(module_spec) #获取已有模型中的宽高要求
    input_depth = hub.get_num_image_channels(module_spec) #获取模型中图片通道深度数
    jpeg_data = tf.placeholder(tf.string, name='DistortJPGInput') #feed_dict输入口
    decoded_image = tf.image.decode_jpeg(jpeg_data, channels=input_depth) #读取图片数据
    decoded_image_as_float = tf.image.convert_image_dtype(decoded_image,tf.float32) #数据类型转换
    decoded_image_4d = tf.expand_dims(decoded_image_as_float, 0) #升维
    
    #对图片数据进行裁切和放缩
    margin_scale = 1.0 + (random_crop / 100.0) #random_crop参数范围0~100
    resize_scale = 1.0 + (random_scale / 100.0) #random_scale参数范围0~100
    margin_scale_value = tf.constant(margin_scale)  #转为张量  
    resize_scale_value = tf.random_uniform(shape=[],minval=1.0,maxval=resize_scale) #转为张量
    scale_value = tf.multiply(margin_scale_value, resize_scale_value)
    precrop_width = tf.multiply(scale_value, input_width)
    precrop_height = tf.multiply(scale_value, input_height)
    precrop_shape = tf.stack([precrop_height, precrop_width])
    precrop_shape_as_int = tf.cast(precrop_shape, dtype=tf.int32)
    precropped_image = tf.image.resize_bilinear(decoded_image_4d,precrop_shape_as_int)
    precropped_image_3d = tf.squeeze(precropped_image, squeeze_dims=[0])
    cropped_image = tf.random_crop(precropped_image_3d,[input_height, input_width, input_depth])
    
    #对图片进行翻转
    if flip_left_right:
        flipped_image = tf.image.random_flip_left_right(cropped_image)
    else:
        flipped_image = cropped_image
        
    #调整图片亮度
    brightness_min = 1.0 - (random_brightness / 100.0) #random_brightness参数范围0~100
    brightness_max = 1.0 + (random_brightness / 100.0)
    brightness_value = tf.random_uniform(shape=[],minval=brightness_min,maxval=brightness_max)
    brightened_image = tf.multiply(flipped_image, brightness_value)
    distort_result = tf.expand_dims(brightened_image, 0, name='DistortResult')
    
    return jpeg_data, distort_result
                    
#入口函数
def main(_):
    tf.logging.set_verbosity(tf.logging.WARN)
    module_spec = hub.load_module_spec(HUB_MODULE)
    graph, bottleneck_tensor, resized_input_tensor, wants_quantization = (
        create_module_graph(module_spec))
    
    with tf.Session(graph=graph) as sess:
        init = tf.global_variables_initializer()
        sess.run(init)
        input_jpeg_tensor,distorted_image_tensor = add_input_distortions(module_spec,True, 40, 60, 36)
        
        result=get_random_distorted_bottlenecks(sess, 5, 'training',
                                                input_jpeg_tensor,distorted_image_tensor,
                                                resized_input_tensor, bottleneck_tensor)
```
打印result得到类似下面的输出：
```
(
    [
        array([0.28729123, 1.5005591 ,  ...,  0.7306035], dtype=float32), 
        array([1.1294909 , 4.1503158 ,  ...,  0.02221665], dtype=float32), 
        array([0.8439883, 2.8368084 ,  ..., 0.04721354], dtype=float32), 
        array([0.00706462, 0.83330685,  ..., 0.99900544], dtype=float32), 
        array([0.00402025, 3.205397  , ..., 0.99900544,], dtype=float32)
    ], #5个被变形后的图片数据
    [2, 1, 3, 0, 0] #对应的5个花类型索引号
)
```
---
##小结
本篇主要添加了以下几个函数用来深入处理bottleneck文件：

* 取得或创建瓶颈文件的函数get_or_create_bottleneck
* 确保瓶颈文件都被缓存的函数cache_bottlenecks
* 随机获取一批bottleneck文件数据get_random_cached_bottlenecks
* 随机获取一批变形的瓶颈数据get_random_distorted_bottlenecks
* 生成变形图片操作ops的函数add_input_distortions


---
###探索人工智能的新边界
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，感谢转发~
---
END







