在前面两篇文章中[Part-1](https://www.jianshu.com/p/2c83da04562f)，[Part-2](https://www.jianshu.com/p/a233a89bc608)，我们编写了很多函数用于读取文件并生成bottleneck文件并随机批量读取。

这一篇我们将继续编写相关的训练、测试函数。

---
##添加最终再训练操作add_final_retrain_ops

我们需要重新训练顶层top layer来识别新的分类，这个函数将向graph添加一些操作，随着一些变量保存权重，然后为所有反向传播设置梯度变化。

这个函数将为训练和计算添加新的softmax和全连接层（密集层）。

增加和修改的代码如下：
```
#添加最终再训练操作ops，一个softmax层一个dense层
#注意这里的quantize_layer为真假值，但必须与create_module_graph(module_spec)得到的wants_quantization一致，否则出错
def add_final_retrain_ops(class_count,final_tensor_name, 
                          bottleneck_tensor,quantize_layer,is_training):
    batch_size, bottleneck_tensor_size = bottleneck_tensor.get_shape().as_list()
    assert batch_size is None, '我们希望针对任意批次大小进行计算'
    with tf.name_scope('input'):
        bottleneck_input = tf.placeholder_with_default(
            bottleneck_tensor,
            shape=[batch_size, bottleneck_tensor_size],
            name='BottleneckInputPlaceholder')
        ground_truth_input = tf.placeholder(tf.int64, [batch_size], name='GroundTruthInput')

    #组织下面的操作使他们在Tensorboard中可见
    layer_name = 'final_retrain_ops'
    with tf.name_scope(layer_name):
        with tf.name_scope('weights'):
            initial_value = tf.truncated_normal( #正态截取，上下不超过0.001*2
                [bottleneck_tensor_size, class_count], stddev=0.001)
            layer_weights = tf.Variable(initial_value, name='final_weights')
            variable_summaries(layer_weights)

        with tf.name_scope('biases'):
            layer_biases = tf.Variable(tf.zeros([class_count]), name='final_biases')
            variable_summaries(layer_biases)

        with tf.name_scope('Wx_plus_b'):
            logits = tf.matmul(bottleneck_input, layer_weights) + layer_biases
            tf.summary.histogram('pre_activations', logits)

    final_tensor = tf.nn.softmax(logits, name=final_tensor_name)
    
    if quantize_layer:
        if is_training:
            tf.contrib.quantize.create_training_graph() #自动重写graph量子化，仅新增的layer被变换，训练用
        else:
            tf.contrib.quantize.create_eval_graph() #预测用
    tf.summary.histogram('activations', final_tensor) #for TensorBoard

    if not is_training: #对于预测，不需要添加损失函数或优化器，所以返回两个None
        return None, None, bottleneck_input, ground_truth_input, final_tensor

    with tf.name_scope('cross_entropy'): #平均交叉熵作为损失函数
        cross_entropy_mean = tf.losses.sparse_softmax_cross_entropy(labels=ground_truth_input, logits=logits)
        tf.summary.scalar('cross_entropy', cross_entropy_mean)

    with tf.name_scope('train'):
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.1) #梯度渐变优化函数
        train_step = optimizer.minimize(cross_entropy_mean)

    return (train_step, cross_entropy_mean, bottleneck_input, ground_truth_input,final_tensor)
                    
#入口函数
def main(_):
    tf.logging.set_verbosity(tf.logging.WARN)
    module_spec = hub.load_module_spec(HUB_MODULE)
    graph, bottleneck_tensor, resized_image_tensor, wants_quantization = (
        create_module_graph(module_spec))
    
    with graph.as_default():
        result = add_final_retrain_ops(5, 'final_tensor_name', 
                                       bottleneck_tensor,wants_quantization, is_training=True)
```

打印result输出下面内容,都是新graph中的各种操节点或张量：
```
(
    <tf.Operation 'train/GradientDescent' type=NoOp>, #train_step
    <tf.Tensor 'cross_entropy/sparse_softmax_cross_entropy_loss/value:0' shape=() dtype=float32>,#cross_entropy_mean
    <tf.Tensor 'input/BottleneckInputPlaceholder:0' shape=(?, 1280) dtype=float32>, #bottleneck_input
    <tf.Tensor 'input/GroundTruthInput:0' shape=(?,) dtype=int64>, #ground_truth_input
    <tf.Tensor 'final_tensor_name:0' shape=(?, 5) dtype=float32> #final_tensor
)
```

---
##执行最终再训练并保存run_final_retrain

从hub读取模型，创建图以及相关操作入口，添加各种操作（训练操作、图片解码等），读取bottleneck数据，然后开始运作，使用变形扭曲的bottleneck数据或者缓存的，sess.run运行训练操作。

同时注意summary信息的保存和checkpoint模型保存。

以下是增加和修改的代码，结合之前代码可以运行:

```
#保存概要和checkpoint路径设置
CHECKPOINT_NAME = os.path.join(dir_path,'checkpoints/retrain')
summaries_dir=os.path.join(dir_path,'summaries/train')

#执行训练兵保存checkpoint的函数
def run_final_retrain(do_distort=True):
    tf.logging.set_verbosity(tf.logging.WARN)
    module_spec = hub.load_module_spec(HUB_MODULE)
    #创建图并获取相关的张量入口
    graph, bottleneck_tensor, resized_image_tensor, wants_quantization = (
        create_module_graph(module_spec))    
    
    with graph.as_default(): 
        #添加训练相关的张量和操作节点入口
        (train_step, cross_entropy, bottleneck_input,ground_truth_input,
         final_tensor) = add_final_retrain_ops(5, 'final_tensor_name', 
                                               bottleneck_tensor,wants_quantization,True)    

    with tf.Session(graph=graph) as sess:
        init = tf.global_variables_initializer()
        sess.run(init)
        
        #添加图片解码相关的张量入口操作
        jpeg_data_tensor, decoded_image_tensor = add_jpeg_decoding(module_spec)
        
        #读取图片的bottleneck数据
        if do_distort:
            distorted_jpeg_data_tensor,distorted_image_tensor=add_input_distortions(module_spec,True,50,50,50)
        else:
            cache_bottlenecks(sess, 
                              jpeg_data_tensor,decoded_image_tensor, 
                              resized_image_tensor,bottleneck_tensor)
        
        #记录概要信息与保存
        train_saver = tf.train.Saver()
        merged = tf.summary.merge_all()
        train_writer = tf.summary.FileWriter(summaries_dir,sess.graph)  
        
        #开始运作！
        for i in range(5):
            #获取图片bottleneck数据
            if do_distort:
                (train_bottlenecks,train_ground_truth) = get_random_distorted_bottlenecks(
                    sess,100, 'training',
                    distorted_jpeg_data_tensor,distorted_image_tensor, 
                    resized_image_tensor, bottleneck_tensor)
            else:
                (train_bottlenecks,train_ground_truth, _) = get_random_cached_bottlenecks(
                    sess, 100, 'training',
                    jpeg_data_tensor,decoded_image_tensor, 
                    resized_image_tensor, bottleneck_tensor)
            
            #启动训练
            train_summary, _ = sess.run([merged, train_step],feed_dict={bottleneck_input: train_bottlenecks,ground_truth_input: train_ground_truth})
            train_writer.add_summary(train_summary, i)
            
        #保存模型    
        train_saver.save(sess, CHECKPOINT_NAME)

#入口函数
def main(_):
        run_final_retrain()

```

运行可能需要几分钟时间，成功后将会生成checkpoints文件夹和summaries文件夹及包含了概要信息和模型文件。
![](imgs/4324074-f657db4732a9fc0e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)




---
##增加评价模型预测精度的操作add_evaluation_step

评价方法需要输入新的图片特征数据和对应的标签，这里的函数接着上面的再训练函数得到的final_tensor, ground_truth_input，作为新的输入口，实现评价功能。

增加和修改的代码如下：

```
#插入评价精确度的操作，返回元组(evaluation step, prediction)
def add_evaluation_step(result_tensor, ground_truth_tensor):
    with tf.name_scope('accuracy'):
        with tf.name_scope('correct_prediction'):
            prediction = tf.argmax(result_tensor, 1) #获取axis=1维度的最大值，即预测结果
            correct_prediction = tf.equal(prediction, ground_truth_tensor) #预测与标签是否相等
        with tf.name_scope('accuracy'):
            evaluation_step = tf.reduce_mean(tf.cast(correct_prediction, tf.float32)) #跨维度计算平均数
    tf.summary.scalar('accuracy', evaluation_step)
    return evaluation_step, prediction
                    
#入口函数
def main(_):
    tf.logging.set_verbosity(tf.logging.WARN)
    module_spec = hub.load_module_spec(HUB_MODULE)
    graph, bottleneck_tensor, resized_image_tensor, wants_quantization = (
        create_module_graph(module_spec))
    
    with graph.as_default():
        (train_step, cross_entropy, bottleneck_input,ground_truth_input, 
         final_tensor) = add_final_retrain_ops(5,'final_tensor_name',bottleneck_tensor, 
                                               wants_quantization,is_training=True)
        
    with tf.Session(graph=graph) as sess: 
        result=add_evaluation_step(final_tensor, ground_truth_input) 

```
打印result的输出是两个张量：

```
(
    <tf.Tensor 'accuracy/accuracy/Mean:0' shape=() dtype=float32>, #evaluation_step
    <tf.Tensor 'accuracy/correct_prediction/ArgMax:0' shape=(?,) dtype=int64> #prediction
)
```
---
##创建用于评估的会话build_eval_session

从存储的训练图checkpoint文件读取变量，恢复到评价图，并利用上面的函数add_evaluation_step添加评估操作。

下面是新增和修改的代码：

```

#保存概要和checkpoint路径设置
CHECKPOINT_NAME = os.path.join(dir_path,'checkpoints/retrain')

#创建和恢复评价会话（没有训练操作），用于导出结果
#返回一个包含评价图的会话，以及相关其他张量和操作
def build_eval_session(module_spec, class_count):
    eval_graph, bottleneck_tensor, resized_input_tensor, wants_quantization = (
        create_module_graph(module_spec))

    eval_sess = tf.Session(graph=eval_graph)
    with eval_graph.as_default(): #添加新的导出层
        (_, _, bottleneck_input,ground_truth_input, 
         final_tensor) = add_final_retrain_ops(class_count, 'final_tensor_name', 
                                               bottleneck_tensor,wants_quantization,is_training=False)
        #把训练图的值恢复到评价图
        tf.train.Saver().restore(eval_sess, CHECKPOINT_NAME)
    
        # 添加评估操作
        evaluation_step, prediction = add_evaluation_step(final_tensor,
                                                      ground_truth_input)

    return (eval_sess, resized_input_tensor, bottleneck_input, ground_truth_input,
          evaluation_step, prediction)  


#入口函数
def main(_):
    tf.logging.set_verbosity(tf.logging.WARN)
    module_spec = hub.load_module_spec(HUB_MODULE)
    graph, bottleneck_tensor, resized_image_tensor, wants_quantization = (
        create_module_graph(module_spec))
    
    with graph.as_default():
        result=build_eval_session(module_spec, 5)
        print(result)
```
输出结果类似如下内容：
```
(
    <tensorflow.python.client.session.Session object at 0x120babdd8>, #sess
    <tf.Tensor 'Placeholder:0' shape=(?, 224, 224, 3) dtype=float32>, #resized_input_tensor
    <tf.Tensor 'input/BottleneckInputPlaceholder:0' shape=(?, 1280) dtype=float32>, #bottleneck_input
    <tf.Tensor 'input/GroundTruthInput:0' shape=(?,) dtype=int64>, #ground_truth_input
    <tf.Tensor 'accuracy/accuracy/Mean:0' shape=() dtype=float32>, #evaluation_step
    <tf.Tensor 'accuracy/correct_prediction/ArgMax:0' shape=(?,) dtype=int64> #prediction
)
```

---
##执行最终评估运算run_final_eval

首先我们需要创建用于评估的会话build_eval_session，然后利用get_random_cached_bottlenecks获取一些随机的图像数据，就可以sess.run运行起来，把bottleneck数据作为feed_dict填充进去了。

下面是增加和修改的代码：

```
#执行最终评估运算
def run_final_eval(sess, module_spec, class_count,
                   jpeg_data_tensor, decoded_image_tensor,
                   resized_image_tensor, bottleneck_tensor):
    #创建评估会话
    (sess, _, bottleneck_input, ground_truth_input, evaluation_step,
     prediction) = build_eval_session(module_spec, class_count)

    #随机获取bottleneck
    test_bottlenecks, test_ground_truth, test_filenames = (
        get_random_cached_bottlenecks(sess, BATCH_SIZE,'testing',
                                      jpeg_data_tensor,decoded_image_tensor, 
                                      resized_image_tensor,bottleneck_tensor))
    #运行评估！
    test_accuracy, predictions = sess.run(
        [evaluation_step, prediction],
        feed_dict={bottleneck_input: test_bottlenecks,#feed_dict
                   ground_truth_input: test_ground_truth})
    
    print('Final test accuracy = %.1f%% (N=%d)' %(test_accuracy * 100, len(test_bottlenecks)))
    print('=== MISCLASSIFIED TEST IMAGES ===')
    for i, test_filename in enumerate(test_filenames):
        if predictions[i] != test_ground_truth[i]:
            print('%70s  %s' % (test_filename,list(image_lists.keys())[predictions[i]])) 
    
#入口函数
def main(_):
    tf.logging.set_verbosity(tf.logging.WARN)
    module_spec = hub.load_module_spec(HUB_MODULE)
    graph, bottleneck_tensor, resized_image_tensor, wants_quantization = (
        create_module_graph(module_spec))
    
    with tf.Session(graph=graph) as sess:
        init = tf.global_variables_initializer()
        sess.run(init)
        jpeg_data_tensor, decoded_image_tensor = add_jpeg_decoding(module_spec)
        run_final_eval(sess, module_spec, 5, 
                       jpeg_data_tensor, decoded_image_tensor, 
                       resized_image_tensor,bottleneck_tensor)
```

运行后会输出一些预测数据，因为在前面run_final_retrain训练中我们只使用了5range，所以精度非常的低：

```python
Final test accuracy = 32.0% (N=100)
=== MISCLASSIFIED TEST IMAGES ===
/Users/zhyuzh/desktop/MyProjects/tfTemp/Retrain/flower_photos/dandelion/142390525_5d81a3659d_m.jpg  daisy
/Users/zhyuzh/desktop/MyProjects/tfTemp/Retrain/flower_photos/tulips/13472393854_b2530f7029_n.jpg  rose
...
```

---
##本篇小结

这里介绍了retrain和eval相关的函数：
* 添加最终再训练操作add_final_retrain_ops
* 执行最终再训练并保存chekcpoint文件run_final_retrain
* 增加评价模型预测精度的操作add_evaluation_step
* 创建用于评估的会话build_eval_session
* 执行最终评估运算run_final_eval

---
###探索人工智能的新边界
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，感谢转发~
---
END


