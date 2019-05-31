savePath='../data'
urlVolumns = 'https://www.jianshu.com/author/notebooks'
params = {'order_by': 'shared_at', 'page': '1'}
headers = '''
accept: application/json
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7
cookie: locale=zh-CN; read_mode=day; default_font=font2; __yadk_uid=0HYqBsZSI5vPl5Uxzq7ZZF8HZMtsAR83; OUTFOX_SEARCH_USER_ID_NCOO=939179854.8824688; ___rl__test__cookies=1550669202339; before-sign-offset-top=0; Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1559013096,1559014439,1559014966,1559015628; remember_user_token=W1s0MzI0MDc0XSwiJDJhJDEwJFYuSVlKelA2LzlaV2luOWFUYVN6UU8iLCIxNTU5MDUxMzQ2LjIzNTM3NjQiXQ%3D%3D--cfed88255535bd740030e5608f5231b341402420; _m7e_session_core=4a55f049234dac513696f42901885bb1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221679fd40aa364f-0c290bd93a9489-113b6653-1296000-1679fd40aa4b8%22%2C%22%24device_id%22%3A%221679fd40aa364f-0c290bd93a9489-113b6653-1296000-1679fd40aa4b8%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22side-banner-click%22%7D%2C%22first_id%22%3A%22%22%7D; Hm_lpvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1559051399
referer: https://www.jianshu.com/writer
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36
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