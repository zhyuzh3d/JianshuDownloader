[React+Electron桌面应用开发文章索引](https://www.jianshu.com/p/71c88b21ea48)

这一篇介绍React网站开发过程中如何发起http请求，从服务端获取数据。

---
##准备工作

安装superagent模块,这是一个可以从服务器获取get数据或者把数据推送post到服务器的工具：
```
zhyuzh$ cnpm i superagent --save-dev
```
[superagent官方开源项目地址](https://github.com/visionmedia/superagent)

在dist目录下创建一个datas/mydata.js用于放置文件，代替服务器接口返回的数json数据，所以最好使用严格的json格式，字段名都带双引号，最后一个字段后面不带逗号：
```
[{
    "title": "标题1",
    "text": "文字内容1"
},{
    "title": "标题2",
    "text": "文字内容2"
}]
```

---
##发起get请求

当元素被添加到页面时候，发起请求,注意这里使用JSON对数据进行了转换.

获取数据之后，使用setState能够让数据立即生效。

HomePage.js中修改的部分:
```
    componentDidMount() {
        let that = this
        superagent.get('datas/mydata.js')
            .end((err, res) => {
                that.setState({
                    mylist: JSON.parse(res.text)
                })
            })
    }
```

在render()方法中，如果使用了mylist数据生成元素（比如用一个list生成多个重复界面元素），setState会在数据读取完成后自动刷新这些元素。

类似下面的代码：
```
let rightItems = []
        for (let i = 0; i < this.state.articleList.length; i++) {
            let data = this.state.articleList[i]
            rightItems.push(h(Grid, {
                item: true,
                xs: 12,
                sm: 6,
                md: 4,
                lg: 3,
            }, [
                h(Card, {
                    className: css.card
                }, h(CardContent, {}, [
                    h(CardMedia, {
                        image: data.image,
                        className: css.cardMedia
                    }),
                    h(CardContent, {
                        style: {
                            padding: 0
                        },
                    }, data.title)
                ]))
            ]))
        }
```

---
###致力于让一切变得简单
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END

