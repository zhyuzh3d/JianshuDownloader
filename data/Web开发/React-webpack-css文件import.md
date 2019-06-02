1. 首先安装```npm i css-loader```
1. 然后修改webpack.conf增加module-rules规则
```
module.exports = {
    entry: './src/index.js', //入口文件
    output: {
        filename: 'bundle.js', //编译后的文件
        path: path.resolve(__dirname, 'dist')
    },
    module: {
        rules: [
            {
                test: /\.css$/,
                loader: ['css-loader']
            }
        ]
    },
    mode: 'development',
    devServer: {
        contentBase: path.join(__dirname, "dist"), //编译好的文件放在这里
        compress: true,
        port: 9000 //本地开发服务器端口
    }
}
```
1. 使用```import css from 'codemirror/lib/codemirror.css'```


---
###致力于让一切变得简单
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END