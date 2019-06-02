首先请阅读和完成
[Tensorflow-iris-案例教程-零基础-机器学习](https://www.jianshu.com/p/b86c020747f9)
在上篇文章中我们每次运行iris.py都会重新训练和测试模型，这很不科学。能不能把训练好的模型保存起来，下次直接使用呢？

--
####checkpoints和SavedModel
Tensorflow可以将训练好的模型以两种形式保存：
1. chekpoints检查点集，依赖于创建模型的代码
1. SavedModel已保存模型，不依赖于创建模型的代码

修改iris.py文件中创建评估器/分类器的代码，添加model_dir保存模型的目录：
 ```
#选定估算器：深层神经网络分类器
models_path=os.path.join(dir_path,'models/')
classifier = tf.estimator.DNNClassifier(
    feature_columns=feature_columns,
    hidden_units=[10, 10],
    n_classes=3,
    model_dir=models_path)
```
保存需要往硬盘写入文件，所以需要操作系统的管理员权限才能运行，在windows下需要右键名利提示符工具选择【以管理员权限运行】：
```
python desktop/iris/iris.py
```
在MacOS下需要加sodu运行，回车后输入系统登陆密码：
```
 sudo python3 ~/desktop/iris/iris.py
```
运行起来后稍等一下模型训练train完成，就可以在桌面iris文件夹下看到一个models文件夹，打开它看起来类似下图的一些文件：
![](http://upload-images.jianshu.io/upload_images/4324074-62e12fe753a37df6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>以前我们没有设定models_dir的时候，tensorflow也会把我们训练的数据放在默认的路径文件夹里，可以print(classifier.model_dir)查看具体地址。

注意到model.ckpt-1和-1000表示在我们训练的第1步step和第1000步都进行了保存，还记得classifier.train(input_fn=lambda:train_input_fn(train_x, train_y,batch_size),steps=1000)中的steps吗？

>注意，如果我们修改了classifier或train的参数（比如hidden_units,batch_size,steps等），就会导致再次运行失败。这时候你需要手工删除models文件夹。

Tensorflow默认每10分钟保存一次，最多保留最近5次，训练第一步step和最后一步step时候一定会保存。

我们可以调整代码修改这个规则,先设定新规则ckpt_config,然后添加到train方法的括号里面config=ckpt_config:
```
#选定估算器：深层神经网络分类器
ckpt_config= tf.estimator.RunConfig(
    save_checkpoints_secs = 60,  # 每60秒保存一次
    keep_checkpoint_max = 10,       # 保留最近的10次
)
models_path=os.path.join(dir_path,'models/')
classifier = tf.estimator.DNNClassifier(
    feature_columns=feature_columns,
    hidden_units=[10, 10],
    n_classes=3,
    model_dir=models_path,
    config=ckpt_config) #
```

--
####恢复使用
从数据文件(data files)输入到估算器训练(estimator,train)，到保存检查点集checkpoints,然后利用保存好的检查点集再进行评估evaluate或应用模型进行预测predict，整个的流程如下图所示：
![](http://upload-images.jianshu.io/upload_images/4324074-955d51fccfbbe93f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

model_dir设置了模型存储的路径，同时，如果已经存储了，那么这也是自动读取模型的路径。
我们把train一行注释掉，然后再运行iris.py，可以发现可以更快速的开始预测，这是因为并没有重新用数据进行训练，而是读取了models文件夹已经存储的模型。
```
#classifier.train(input_fn=lambda:train_input_fn(train_x, train_y,batch_size),steps=1000)
```

--
#### 整理文件
当然我们可以将整个iris文件拆分成2个文件
 iris.load
1. 读取两个数据文件
1. 提供.load载入方法
1. 提供.train_input_fn训练数据“喂食”方法
1. 提供.eva_input_fn评估数据“喂食”方法
```
import os
import pandas as pd
import tensorflow as tf

FUTURES = ['SepalLength', 'SepalWidth','PetalLength', 'PetalWidth', 'Species']
SPECIES = ['Setosa', 'Versicolor', 'Virginica']
    
#格式化数据文件的目录地址
dir_path = os.path.dirname(os.path.realpath(__file__))
train_path=os.path.join(dir_path,'iris_training.csv')
test_path=os.path.join(dir_path,'iris_test.csv')
    
#载入数据函数
def load():    
    #载入训练数据
    train = pd.read_csv(train_path, names=FUTURES, header=0)
    train_x, train_y = train, train.pop('Species')

    #载入测试数据
    test = pd.read_csv(test_path, names=FUTURES, header=0)
    test_x, test_y = test, test.pop('Species') 
    
    return (train_x, train_y),(test_x, test_y)    
    
#针对训练的喂食函数
def train_input_fn(features, labels, batch_size):
    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))
    dataset = dataset.shuffle(1000).repeat().batch(batch_size) #每次随机调整数据顺序
    return dataset


#针对测试的喂食函数
def eval_input_fn(features, labels, batch_size):
    features=dict(features)
    inputs=(features,labels)
    dataset = tf.data.Dataset.from_tensor_slices(inputs)
    dataset = dataset.batch(batch_size)
    return dataset
```

iris_premade.py
1. estamator()函数用于根据my_cfg设置生成估算分类器classifier
1. train()函数执行训练命令，用户输入自定义四个设置如10,10,100,1000
1. evalute()函数执行评估命令，对训练的模型进行评估
1.predict()函数执行预测命令，对输入的四个测量数据进行评估

```
import os
import tensorflow as tf
import iris_load as dts
import shutil

#利用iris_load.py读取训练数据和测试数据
(train_x, train_y), (test_x, test_y) = dts.load()
    
#设定特征值的名称
feature_columns = []
for key in train_x:
    feature_columns.append(tf.feature_column.numeric_column(key=key))   

#估算器存储路径
dir_path = os.path.dirname(os.path.realpath(__file__))
models_path=os.path.join(dir_path,'models/')

#估算器存储设置选项
ckpt_config= tf.estimator.RunConfig(
    save_checkpoints_secs = 60,  #每60秒保存一次
    keep_checkpoint_max = 10,    #保留最近的10次
)

#估算器预设
my_cfg=dict() 
my_cfg['layer1'],my_cfg['layer2'],my_cfg['batch_size'],my_cfg['steps']=10,10,100,1000

#生产估算器函数：深层神经网络分类器
def estimator():
    classifier = tf.estimator.DNNClassifier(
        feature_columns=feature_columns,
        hidden_units=[my_cfg['layer1'], my_cfg['layer2']],
        n_classes=3,
        model_dir=models_path,
        config=ckpt_config)
    return classifier 

#训练模型函数
def train():
    print('Please input:layer1 nodes,layer2 nodes,batch_size,steps')
    params=input().split(',')
    if len(params)>3:
        if os.path.exists(models_path):
            print('Removing models folder...')
            shutil.rmtree(models_path) #移除models目录
            
        my_cfg['layer1'],my_cfg['layer2'],my_cfg['batch_size'],my_cfg['steps'] = map(int, params)
        
    print('Training...')
    classifier=estimator()   
    classifier.train(input_fn=lambda:dts.train_input_fn(
            train_x,
            train_y,
            my_cfg['batch_size']),
         steps=my_cfg['steps'])
    print('Train OK')         
        

#评估模型函数
def evalute():
    print('Evaluating...') 
    classifier=estimator()  
    eval_result = classifier.evaluate(
        input_fn=lambda:dts.eval_input_fn(test_x, test_y,my_cfg['batch_size']))
    print('Evaluate result:',eval_result)
    
def predict():
    print('Please enter features: SepalLength,SepalWidth,PetalLength,PetalWidth;0 for exit.')
    params=input().split(',');
    if len(params)>3:
        predict_x = {
            'SepalLength': [float(params[0])],
            'SepalWidth': [float(params[1])],
            'PetalLength': [float(params[2])],
            'PetalWidth': [float(params[3])],
        }    

        #进行预测
        classifier=estimator()        
        predictions = classifier.predict(
                input_fn=lambda:dts.eval_input_fn(predict_x,
                                                labels=[0],
                                                batch_size=my_cfg['batch_size']))

        #预测结果是数组，尽管实际我们只有一个
        for pred_dict in predictions:
            class_id = pred_dict['class_ids'][0]
            probability = pred_dict['probabilities'][class_id]
            print('Predict result:',dts.SPECIES[class_id],100 * probability)
    else:
        print('Input format error,ignored.')

#定义入口主函数
def main(args):
    while 1==1:
        print('Please enter train,evalute or predict:')
        cmd = input() #捕获用户输入的数字
        if cmd=='train':
            train()
        elif cmd=='evalute':
            evalute()
        elif cmd=='predict':
            predict()
        elif cmd=='retrain':
            retrain()
            
#运行主函数            
if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run(main)
```

注意my_cfg=dict() 这个字典数据用法，它和下面一行生成类似下面这种数据结构
```
my_dict={
  'layer1':10,
  'layer2':10,
  'batch_size':100,
  'steps':1000
}
```

然后我们才能在def定义的函数中修改它并使其在estimator()方法中生效。
>def定义的函数里面无法直接修改外面的数据，比如下面代码，打印出来是100而不是99
```
a=100
def change():
    a=99
print(a)
```
>同样，下面的代码输出的是101，而不是11:
```
n=100

def estimator():
    b=n+1
    print(b)
    
def train():
    n=10

def evalute():
    estimator()
    
train() #这行并不能真正改变n
evalute()
```
>所以，如果不使用dict字典，那么当我们在train训练时候改变参数(hidden_units,batch_size,steps)的时候，evalute和predict都不能使用到这些参数。

如果遇到问题，您也可以点击[这里]( https://pan.baidu.com/s/1pwfoL-gXhHxmFQh7HUmgHg)直接下载代码
提取密码: 83qe

---
###探索人工智能的新边界
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，感谢转发~
---
END



