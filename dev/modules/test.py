import os
def  readHeaders(): #读取设置文件并填充到界面
    fpath=os.getcwd()+'/config.txt'
    if os.path.exists(fpath):
        f=open(fpath,'r')
        hdrs=f.read()
        print(hdrs)
        #iptHeader.insert(INSERT,hdrs)

readHeaders()