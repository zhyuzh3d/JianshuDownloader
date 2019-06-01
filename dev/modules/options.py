savePath='../data'
urlVolumns = 'https://www.jianshu.com/author/notebooks'
params = {'order_by': 'shared_at', 'page': '1'}
headers = '''
请复制粘贴您浏览器的headers信息
'''
def str2obj(s, s1=';', s2='='):
    li = s.split(s1)
    res = {}
    for kv in li:
        li2 = kv.split(s2)
        if len(li2) > 1:
            res[li2[0]] = li2[1]
    return res

headers = str2obj(headers, '\n', ': ')

#...