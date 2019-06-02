>[点击这里进入**人工智能DBD嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---
这可能是爬虫技术无法破解的加密格式。

##案例分析

以[**58房产网站**](https://su.58.com/zufang/pn2/?PGTID=0d300008-0000-5965-8ce1-1873463f7758&ClickID=1)为例,我们爬取的房价以及其他很多数字都是乱码，**閏龤龤龤元/月**，**龒室龤厅龒卫龥龤㎡**。

右键检查元素会发觉，看上去正常的数字，在html代码中却是乱码。
![](imgs/4324074-d462f6ff474046bf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

右侧可以注意到这样的元素使用了奇怪的`font-family:fangchan-secret`(房产-加密)字体样式，如果我们关闭这个`strongbox`样式，停用这个字体，页面上就会如实的显示乱码了。

![](imgs/4324074-e00bb38a0c6e7795.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

`font-family`这是一种自定义字体，它可以把乱码显示成正常的数字。
>这是一种有效的反爬虫方式，但我还是要鄙视这种处理方式，首先这种乱码对搜索引擎非常不友好，其次用户在页面上复制粘贴得到的也是乱码，用户体验不友好，另外在真的要显示乱码所用字符的极端情况下将无法实现，所以这种手段仅适合加密少量字符。

##问题分析

右键查看页面源代码，搜索`fangchan-secret`可以看到这个字体是JavaScript临时生成的。
![](imgs/4324074-2897e3f7afbe3c4f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

主要的字体信息是一长段大小写字母，我们把它完整复制下来。
为Python安装fonttools字体工具模块，`conda install -c mwcraig fonttools`，然后使用下面的代码将这段字母存储为ttf字体文件，中间的key部分需要你手工替换。
```
from fontTools.ttLib import TTFont
import base64
import io

key='''
AAEAAAALAIAAAwAwR1N.........AAA 
'''
data = base64.b64decode(key) #base64解码
fonts = TTFont(io.BytesIO(data)) #生成二进制字节
fonts.save('fangchan-secret.ttf')
```
然后打开[**百度字体编辑网站**](http://fontstore.baidu.com/static/editor/index.html)，用打开按钮选择刚才生成的`fangchan-secret.ttf`,就可以看到真实的字体内容。

![](imgs/4324074-3fbe8165c7cd010a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们看到每个字形都有一个蓝色的编码，如`$9A4B`这样的字符，这是字符的16进制编码，用`chr()`命令查看它的真正样子。
![](imgs/4324074-79106f6442b17c6f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这就是说，`fangchan-secret`字体把罕见的字符显示为0~9数字了。

## 解决方案

对字体数据进一步处理。
```
cmap=fonts.getBestCmap() #十进制ascii码到字形名的对应
for char in cmap:
    print(char,hex(char),chr(char),cmap[char])
```
这个代码输出类似下面这个内容：
![](imgs/4324074-88482634ed58d24c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

其中各个内容的关系如下图（上面的输出并没有包含字形图）：
![](imgs/4324074-fc08228ae7abd823.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


我们可以从字体文件中找到字符、编码和字形名，可以用工具查看到字形图，但如何把`0x9476`对应到`6`这个数字就只能靠人眼识别了，这也是加密的意义所在了。——我们无法用代码直接实现字符到字形所表示数字的对应关系。

这是死穴。

但很多时候没有那么糟糕，毕竟只是10个数字被加密，我们只要凭人眼建立10个字符乱码到真实数字的对应关系就可以解决问题，例如，假设我们搞定这个字典就不怕了：

```
numdict={
    '鑶':0,
    '閏':1,
    '餼':2,
    '驋':3,
    '鸺':4,
    '麣':5,
    '齤':6,
    '龒':7,
    '龤':8,
    '龥':9
}
```
但对于58房产网，这样还不够，因为他们的网站会每隔几秒钟就变化`fangchan-secret`的`key`，就是那一长串`AAEAAAALAIAAAwAwR1N.........AAA`。

反复对比之后发觉，**它只是随机变化字符`龥...`和字形名`glyph00007...`之间的对应关系，而字形名和字形之间的关系并不变，比如说`glyph00007`几秒前对应`龒`几秒后又对应`齤`，但它总是对应字形`6`这个不变**。

也就是说下面这个对应是固定的：
```
glyphdict = {
    'glyph00001': '0',
    'glyph00002': '1',
    'glyph00003': '2',
    'glyph00004': '3',
    'glyph00005': '4',
    'glyph00006': '5',
    'glyph00007': '6',
    'glyph00008': '7',
    'glyph00009': '8',
    'glyph00010': '9'
}
```

而实际上我们可以从`fongchan-secret`中读取到字符和字形名之间的对应关系，类似：
```
chrdict={
    '鑶':'glyph00006',
    '閏':'glyph00004',
    '餼':'glyph00001',
    '驋':'glyph00002',
    '鸺':'glyph00003',
    '麣':'glyph00009',
    '齤':'glyph00010',
    '龒':'glyph00008',
    '龤':'glyph00007',
    '龥':'glyph00005'
}
```
综上我们就可以间接实现乱码到数字的转换了。

##最终代码

首先注意这个multReplace多个替换函数的作用：
```
#使用字典批量替换
import re

def multReplace(text, rpdict):
    rx = re.compile('|'.join(map(re.escape, rpdict)))
    return rx.sub(lambda match:rpdict[match.group(0)], text)
```
它可以批量执行replace的功能。rx是一个竖线分割的**或者**表达式，比如`'a|b|c|d`，这个表达式可以匹配出符合abcd任何一个字母匹配的列表。
`rx.sub()`方法传入了一个`lambda`函数，表示可以对rx匹配列表中的每个匹配都执行一个替换，效果如下：
![](imgs/4324074-05169d8644718f68.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

下面是解密字体函数：

```
#解密58房产的字体加密
from fontTools.ttLib import TTFont
import base64
import re
import io

def decode58Fangchan(html,key):
    glyphdict = {
        'glyph00001': '0',
        'glyph00002': '1',
        'glyph00003': '2',
        'glyph00004': '3',
        'glyph00005': '4',
        'glyph00006': '5',
        'glyph00007': '6',
        'glyph00008': '7',
        'glyph00009': '8',
        'glyph00010': '9'
    }    
    data = base64.b64decode(key)  #base64解码
    fonts = TTFont(io.BytesIO(data))  #生成二进制字节
    cmap = fonts.getBestCmap()  #十进制ascii码到字形名的对应{38006:'glyph00002',...}
    chrMapNum = {}  #将变为{‘龥’:'1',...}
    for asc in cmap:
        chrMapNum[chr(asc)] = glyphdict[cmap[asc]]

    return multReplace(html,chrMapNum)
```
读取本地爬取的文件进行解密：
```
from bs4 import BeautifulSoup
import html
with open('./pages/2.html', 'r') as f:
    text = html.unescape(f.read())  #将&#x958f;室变为閏室
    key = re.findall(r"base64,(.*)'\).format", text)[0]  #用正则表达式提取AAE..AAA
    dehtml = decode58Fangchan(text, key)
    soup = BeautifulSoup(dehtml)
    moneyTags = soup.find_all('div', 'money')
    print(','.join([m.b.text.strip() for m in moneyTags]))
```
输出结果如下所示：
![](imgs/4324074-e5ecabfb485d5181.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如果不进行字体解密的乱码结果如下：
![](imgs/4324074-9d2ef4f0efa911ba.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##动态字体

这样的字体加密文件如何实现的？
这里是一些思路和资源：

1. **把多个svg文件合成为svg字体**。Nodejs可以使用[**svgtofont**](https://www.npmjs.com/package/svgtofont)模块，依照官方案例，把从网站下载（如[iconfont网站](https://www.iconfont.cn)）的多个svg图形文件放到icon文件夹下，然后执行node代码就会得到一个可以读懂的.svg文件，类似以下文件，可以清楚地看到它包含了三个字形glyph以及每个字形对应的unicode代码，而长串的数字就是svg图形数据。（你也可以从iconfont购物车直接下载得到这个文件）
```
<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd" >
<svg xmlns="http://www.w3.org/2000/svg">
<defs>
  <font id="svgtofont" horiz-adv-x="200">
    <font-face font-family="svgtofont"
      units-per-em="200" ascent="200"
      descent="0" />
    <missing-glyph horiz-adv-x="0" />
    <glyph glyph-name="iconfont-zan"
      unicode="&#x9476;"
      horiz-adv-x="200" d="M35.9453333984375 156.107777734375C43.2013333984375 162.9566666015625 52.8688888671875 167.1971111328125 62.828222265625 167.868222265625C70.7455556640625 168.480222265625 78.81244453125 166.806666796875 85.8811111328125 163.212C91.2586666015625 160.535777734375 95.9453333984375 156.63044453125 99.868 152.1026666015625C104.1108888671875 156.99755546875 109.25755546875 161.18755546875 115.197777734375 163.8404443359375C119.3948888671875 165.933333203125 124.0051111328125 167.031333203125 128.622222265625 167.7128888671875C139.672666796875 168.992222265625 151.196 165.966222265625 160.0631111328125 159.219777734375C170.44844453125 151.5731111328125 177.136 139.121777734375 177.6586666015625 126.223333203125C178.3591111328125 112.040888671875 173.656 97.919333203125 165.585777734375 86.3371109375C160.102222265625 78.316888671875 153.19 71.384888671875 145.85755546875 65.0582220703125C135.7428888671875 56.4326666015625 124.6102220703125 49.1366666015625 113.6102220703126 41.72155546875C108.8542220703126 38.6026666015625 104.313333203125 35.179777734375 99.8682220703125 31.637333203125C95.1782220703125 35.39155546875 90.3526666015626 38.969777734375 85.3291109375001 42.2606666015625C73.5079998046875 50.2248888671875 61.525333203125 58.08355546875 50.9282220703125 67.667777734375C41.0062220703125 76.55155546875 32.13555546875 87.0088888671875 26.962888671875 99.4046666015625C24.79266640625 104.53755546875 23.3179998046875 109.9611111328125 22.5575552734375 115.47755546875C21.8891107421875 120.7891109375 21.710221875 126.2162220703125 22.6495552734375 131.505333203125C24.224 140.8673333984375 28.9931111328125 149.6486666015625 35.9453333984375 156.107777734375L35.9453333984375 156.107777734375zM56.0746666015625 159.857777734375" />
    <glyph glyph-name="iconfont"
      unicode="&#xEA02;"
      horiz-adv-x="200" d="M65.01953125 18.8671875H134.4140625C140.80078125 18.8671875 145.7421875 24.21875 145.7421875 30.625V65.1953125H53.6328125V30.625C53.6328125 24.23828125 58.65234375 18.8671875 65.01953125 18.8671875zM134.4140625 180.76171875H65.01953125C58.6328125 180.76171875 53.6328125 175.78125 53.6328125 169.39453125V134.98046875H145.76171875V169.39453125C145.7421875 175.78125 140.78125 180.76171875 134.4140625 180.76171875zM157.3828125 134.98046875V123.1640625H41.9921875V134.98046875H30.33203125C23.9453125 134.98046875 18.92578125 129.53125 18.92578125 123.125V42.1875C18.92578125 35.80078125 23.9453125 30.5078125 30.33203125 30.5078125H41.9921875V76.8359375H157.36328125V30.5078125H169.08203125C175.46875 30.5078125 180.80078125 35.80078125 180.80078125 42.1875V123.125C180.80078125 129.51171875 175.46875 134.98046875 169.08203125 134.98046875H157.3828125zM157.3828125 99.7265625H122.8515625V111.54296875H157.3828125V99.7265625z" />
    <glyph glyph-name="iconfont_info"
      unicode="&#xEA03;"
      horiz-adv-x="200" d="M200 100C199.3625 71.625 189.625 48.0375 170.7875 29.2125C151.9625 10.375 128.375 0.625 100 0C71.625 0.6375 48.0375 10.375 29.2125 29.2125C10.375 48.0375 0.625 71.625 0 100C0.6375 128.375 10.375 151.9625 29.2125 170.7875C48.0375 189.625 71.625 199.375 100 200C128.375 199.3625 151.9625 189.625 170.7875 170.7875C189.625 151.9625 199.375 128.375 200 100zM100 112.5A12.5 12.5 0 0 1 87.5 100V50A12.5 12.5 0 0 1 112.5 50V100A12.5 12.5 0 0 1 100 112.5zM100 137.5A12.5 12.5 0 1 1 100 162.5A12.5 12.5 0 0 1 100 137.5z" />
  </font>
</defs>
</svg>
```
2. **修改unicode改变字符和字形的对应关系**，你可以使用任意语言直接修改这个类似html格式的svg文件。
2.  **把svg字体文件转为ttf**。Nodejs可以使用[**svg2ttf模块**](https://www.npmjs.com/package/svg2ttf)，把第一步生成的svg文件转为ttf字体文件。
2. **使用base64解码读取ttf**。在macOS下可以直接使用终端命令`base64 a.svg > a.txt`获得base64编码，或者使用Python或其他语音进行base64编码。以下是txt文件的样子。
```python
AAEAAAALAIAAAwAwR1N........YW4IaWNvbmZvbnQNaWNvbmZvbnRfaW5mbwAAAAAA
```
5. **将上面的base64代码嵌入到html页面**。参照以下index.html代码（可直接单独使用）:
```
<style>
    @font-face {
        font-family: "myfont";
        src: url(data:application/x-font-woff;charset=utf-8;base64,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);
        font-style: normal;
        font-weight: 400;
    }

</style>
<a style="font-family: myfont">图标字体：&#x9476;&#xEA02;&#xEA03;</a>

```
 页面效果如下：
![](imgs/4324074-2f72ad387383b2ca.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


##其他资源

[**字体松鼠fontsquirrel**](https://www.fontsquirrel.com/tools/webfont-generator)，可以自定义字形包，直接下载得到base64数据，注意要选择expert才能看到base64选项。
[**fontello**](http://fontello.com/),同样可以上传自己的svg或者点击网站现有的图标（一定要点），点了之后就可以Customize Codes自定义修改了，58房产就是用的这个网站的API。
[**百度字体编辑器**](http://fontstore.baidu.com/static/editor/index.html)，功能相似，可以打开现有ttf，也可以深度编辑字形和字符，然后下载ttf或其他字体格式。
[**阿里iconfont图标库**](https://www.iconfont.cn)，可以下载数十万各种图标素材，记得一定要加入购物车，然后从购物车下载，可以直接得到svg字体文件。

>结语，使用这种字体加密反爬其实没有太多意义，网站既然是公开的，又为什么害怕别人知道你的公开数据呢？但这种加密方法是很强悍的，如果动态扰乱字形名那就真的无解了，如果有的话就只能靠字符图像识别技术了。动态扰乱字形名和字形之间的关系，可以在需要极端保密的场景下真正实现每个页面显示的信息动态加密，当然字形太多的话base64字符数据也会很多，下载很慢。

---
>[点击这里进入**人工智能DBD嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END