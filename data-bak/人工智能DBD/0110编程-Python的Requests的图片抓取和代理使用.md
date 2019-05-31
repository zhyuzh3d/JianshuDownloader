>[点击这里进入**人工智能嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---

##图片抓取与存储
注意文件名和存储位置。
```
import requests
url='https://extraimage.net/images/2019/01/07/12a17ccb9a28f2e9cf4d13942a1929d0.jpg'
res=requests.get(url)
img=res.content
with open( 'data/test.jpg','wb' ) as f:
    f.write(img)
print('OK')
```
使用PIL显示图片。
```
from PIL import Image
im = Image.open('data/test.jpg')
im
```

## 代理使用
[可以使用西刺免费代理IP](https://www.xicidaili.com/)获得代理地址和端口号，注意经常不稳定无法连接，还要注意优先改为http而不是https。
```
import requests
from bs4 import BeautifulSoup
import time

url='https://movie.douban.com/top250'
proxy = {
    'http': 'http://119.101.113.239:9999'
}
header = {
    'User-agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
}
res = requests.get(url,headers=header, proxies=proxy)
soup = BeautifulSoup(res.text)
movies = soup.find_all('div', 'info')
print(movies[0])
```


---
>[点击这里进入**人工智能DBD嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END