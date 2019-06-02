报错：
```NPM Unexpected end of JSON input while parsing near```
```npm ERR! A complete log of this run can be found in:```

解决方案：
```npm install --registry=https://registry.npm.taobao.org --loglevel=silly```
```npm cache clean --force```

然后再正常安装
```sudo npm install -g cnpm --registry=https://registry.npm.taobao.org```
