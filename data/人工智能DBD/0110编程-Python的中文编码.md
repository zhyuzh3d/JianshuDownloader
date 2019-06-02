>[点击这里进入**人工智能嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---

收集的一些常用中文乱码转换：
```
print("ord('我'):",ord('我'))
print("chr(25105):",chr(25105))
print('\n')
print("'我的简书'.encode('unicode_escape'):",'我的简书'.encode('unicode_escape'))
print("'\\u6211\\u7684\\u7b80\\u4e66'.encode().decode('unicode_escape'):",'\\u6211\\u7684\\u7b80\\u4e66'.encode().decode('unicode_escape'))
print("'\\u6211\\u7684\\u7b80\\u4e66'.encode('ascii').decode('unicode_escape'):",'\\u6211\\u7684\\u7b80\\u4e66'.encode('ascii').decode('unicode_escape'))

print('\n')
print("'我的简书'.encode('gbk').decode('ISO-8859-1'):",'我的简书'.encode('gbk').decode('ISO-8859-1'))
print("'ÎÒµÄ¼òÊé'.encode('ISO-8859-1'):",'ÎÒµÄ¼òÊé'.encode('ISO-8859-1'))
print(r"'\xce\xd2\xb5\xc4\xbc\xf2\xca\xe9'.encode('ISO-8859-1').decode('gbk'):",'\xce\xd2\xb5\xc4\xbc\xf2\xca\xe9'.encode('ISO-8859-1').decode('gbk'))
print("'ÎÒµÄ¼òÊé'.encode('ISO-8859-1').decode('gbk'):",'ÎÒµÄ¼òÊé'.encode('ISO-8859-1').decode('gbk'))
print('\n')
print("'我的简书'.encode('utf-8').decode('utf-16'):",'我的简书'.encode('utf-8').decode('utf-16'))
print("'裦\ue791蒚껧\ue480ꚹ'.encode('utf-16').decode('utf8','ignore'):",'裦\ue791蒚껧\ue480ꚹ'.encode('utf-16').decode('utf8','ignore'))
```
输出结果：
```
ord('我'): 25105
chr(25105): 我


'我的简书'.encode('unicode_escape'): b'\\u6211\\u7684\\u7b80\\u4e66'
'\u6211\u7684\u7b80\u4e66'.encode().decode('unicode_escape'): 我的简书
'\u6211\u7684\u7b80\u4e66'.encode('ascii').decode('unicode_escape'): 我的简书


'我的简书'.encode('gbk').decode('ISO-8859-1'): ÎÒµÄ¼òÊé
'ÎÒµÄ¼òÊé'.encode('ISO-8859-1'): b'\xce\xd2\xb5\xc4\xbc\xf2\xca\xe9'
'\xce\xd2\xb5\xc4\xbc\xf2\xca\xe9'.encode('ISO-8859-1').decode('gbk'): 我的简书
'ÎÒµÄ¼òÊé'.encode('ISO-8859-1').decode('gbk'): 我的简书


'我的简书'.encode('utf-8').decode('utf-16'): 裦蒚껧ꚹ
'裦蒚껧ꚹ'.encode('utf-16').decode('utf8','ignore'): 我的简书
```

>如果去掉ignore,`'裦\ue791蒚껧\ue480ꚹ'.encode('utf-16').decode('utf8')`将抛出异常`UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte`

> ord和chr互为相反，字符和ascii码互换
斜杠加四位的乱码可以.encode().decode('unicode_escape')恢复
斜杠加两位的乱码可以用.encode('ISO-8859-1').decode('gbk')恢复
类似拼音的乱码可以用.encode('ISO-8859-1').decode('gbk')恢复
类似古文的乱码可以用.encode('utf-16').decode('utf8','ignore')



---
>[点击这里进入**人工智能DBD嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END