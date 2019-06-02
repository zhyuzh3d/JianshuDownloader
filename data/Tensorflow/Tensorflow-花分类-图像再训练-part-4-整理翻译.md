继续前面的三篇文章[Part-1](https://www.jianshu.com/p/2c83da04562f)，[Part-2](https://www.jianshu.com/p/a233a89bc608)，[Part-3](https://www.jianshu.com/p/bdb87070b780)，这一篇我们来完善存储和恢复机制。

---
##把计算图保存到文件save_graph_to_file

下面是增加的代码，先不要运行，稍后一起测试：
```
#将图保存到文件,必要时创建允许的量子化    
def save_graph_to_file(graph, graph_file_name, module_spec, class_count):
    sess, _, _, _, _, _ = build_eval_session(module_spec, class_count)
    graph = sess.graph

    output_graph_def = tf.graph_util.convert_variables_to_constants(
        sess, graph.as_graph_def(), ['final_tensor_name'])

    with tf.gfile.FastGFile(graph_file_name, 'wb') as f:
        f.write(output_graph_def.SerializeToString())  
```

---
##保存评估模型export_model

注意每次使用前必须把旧的saved_model文件夹删除或改名。
```
#导出评估eval图的模型pd文件用于提供服务
saved_model_dir=os.path.join(dir_path,'saved_model'+str(datetime.now()))
def export_model(module_spec, class_count):
    sess, in_image, _, _, _, _ = build_eval_session(module_spec, class_count)
    graph = sess.graph
    with graph.as_default():
        #输入输出点
        inputs = {'image': tf.saved_model.utils.build_tensor_info(in_image)}
        out_classes = sess.graph.get_tensor_by_name('final_tensor_name:0')
        outputs = {
            'prediction': tf.saved_model.utils.build_tensor_info(out_classes)
        }
        #创建签名
        signature = tf.saved_model.signature_def_utils.build_signature_def(
            inputs=inputs,
            outputs=outputs,
            method_name=tf.saved_model.signature_constants.PREDICT_METHOD_NAME)

        #初始化
        legacy_init_op = tf.group(tf.tables_initializer(), name='legacy_init_op')

        #保存saved_model
        builder = tf.saved_model.builder.SavedModelBuilder(saved_model_dir)
        builder.add_meta_graph_and_variables(
            sess, [tf.saved_model.tag_constants.SERVING],
            signature_def_map={
                tf.saved_model.signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY:signature
            },
            legacy_init_op=legacy_init_op)
    builder.save()

```

---
##改进最终再训练函数

最后我们把run_final_retrain函数改进一下，增加评估eval和保存、导出功能。
>注意每次使用前必须把旧的saved_model文件夹删除或改名。

以下是修改后的代码（这里参数train_steps=10，所以得到的模型精度也非常糟糕。如果您的计算机允许，官方默认是4000，请量力而为）：
```
#保存概要和checkpoint路径设置
CHECKPOINT_NAME = os.path.join(dir_path,'checkpoints/retrain')
summaries_dir=os.path.join(dir_path,'summaries/train')
ensure_dir_exists(os.path.join(dir_path,'output')) 
saved_model_path=os.path.join(dir_path,'output/out_graph.pd')
output_label_path=os.path.join(dir_path,'output/labels.txt')

#执行训练兵保存checkpoint的函数
def run_final_retrain(train_steps=10,
             eval_step_interval=5,
             do_distort=True):
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
            
        #创建评估新层精度的操作
        evaluation_step, _ = add_evaluation_step(final_tensor, ground_truth_input)
        
        #记录概要信息与保存
        train_saver = tf.train.Saver()
        merged = tf.summary.merge_all()
        train_writer = tf.summary.FileWriter(summaries_dir+'/retrain',sess.graph)      
        validation_writer = tf.summary.FileWriter(summaries_dir + '/validation')        
        
        #开始运作！
        for i in range(train_steps):
            #获取图片bottleneck数据
            if do_distort:
                (train_bottlenecks,train_ground_truth) = get_random_distorted_bottlenecks(
                    sess,BATCH_SIZE, 'training',
                    distorted_jpeg_data_tensor,distorted_image_tensor, 
                    resized_image_tensor, bottleneck_tensor)
            else:
                (train_bottlenecks,train_ground_truth, _) = get_random_cached_bottlenecks(
                    sess, BATCH_SIZE, 'training',
                    jpeg_data_tensor,decoded_image_tensor, 
                    resized_image_tensor, bottleneck_tensor)
            
            #启动训练
            train_summary, _ = sess.run(
                [merged, train_step],
                feed_dict={bottleneck_input: train_bottlenecks,
                           ground_truth_input: train_ground_truth})
            train_writer.add_summary(train_summary, i)
            
            #间隔性启动评估
            is_last_step = (i + 1 == train_steps)
            if (i % eval_step_interval) == 0 or is_last_step:
                train_accuracy, cross_entropy_value = sess.run(
                    [evaluation_step, cross_entropy],
                    feed_dict={bottleneck_input: train_bottlenecks,
                               ground_truth_input: train_ground_truth})
                
                tf.logging.info('%s: Step %d: Train accuracy = %.1f%%' %(datetime.now(), i, train_accuracy * 100))
                tf.logging.info('%s: Step %d: Cross entropy = %f' %(datetime.now(), i, cross_entropy_value))
            
                #使用不同的bottleneck数据进行评估
                validation_bottlenecks, validation_ground_truth, _ = (
                    get_random_cached_bottlenecks(
                        sess, 10, 'validation', 
                        jpeg_data_tensor,decoded_image_tensor, 
                        resized_image_tensor, bottleneck_tensor))
                #启动评估！
                validation_summary, validation_accuracy = sess.run(
                    [merged, evaluation_step],
                    feed_dict={bottleneck_input: validation_bottlenecks,
                               ground_truth_input: validation_ground_truth})
                
                validation_writer.add_summary(validation_summary, i)
                tf.logging.info('%s: Step %d: Validation accuracy = %.1f%% (N=%d)' %(datetime.now(), i, validation_accuracy * 100,len(validation_bottlenecks)))            
            
        
            #间隔保存中介媒体文件，为训练保存checkpoint
            if (i % eval_step_interval == 0 and i > 0):
                train_saver.save(sess, CHECKPOINT_NAME)
                intermediate_file_name = (os.path.join(dir_path + 'intermediate') + str(i) + '.pb')
                tf.logging.info('Save intermediate result to : '+intermediate_file_name)
                save_graph_to_file(graph, intermediate_file_name, module_spec,5)

        #保存模型    
        train_saver.save(sess, CHECKPOINT_NAME)        
        
        #执行最终评估
        run_final_eval(sess, module_spec, 5,
                       jpeg_data_tensor, decoded_image_tensor,
                       resized_image_tensor,bottleneck_tensor)

        
        tf.logging.info('Save final result to : ' + saved_model_path)
        if wants_quantization:
            tf.logging.info('The model is instrumented for quantization with TF-Lite')
        save_graph_to_file(graph, saved_model_path, module_spec, 5)
        with tf.gfile.FastGFile(output_label_path, 'w') as f:
            f.write('\n'.join(image_lists.keys()) + '\n')
        export_model(module_spec, 5)
```

---
##案例小结

这个案例来自Tensorflow官方教程，之前两个相对都比较简单，代码量只有100行左右，这个案例官方原代码突然有1300行之多，大有才学了十以内加减法然后就讲微积分方程的感觉。

这里整个案例去掉了很多官方代码中我认为无关紧要的部分，仍然有600多行，如果有时间我还会在整理这个案例，希望能只保留关键流程代码，两三百行不能再多了。

已经读到这里的用户实属难得，如果遇到困难，请从[百度网盘下载](https://pan.baidu.com/s/1peJ568BGJjS7UxnANzW0XQ)(密码:lzjg)直接下载final.py文件使用。请注意文件读写权限，每次运行前请删除saved_model文件夹。

---
###探索人工智能的新边界
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，感谢转发~
---
END



