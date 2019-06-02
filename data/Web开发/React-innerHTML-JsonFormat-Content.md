在React内如何正常显示格式化的json对象？

* 首先安装json-pretty-html，他能将json对象格式化成漂亮的html标签代码
* 然后使用react的自带dangerouslySetInnerHTML属性加入代码

主要代码：
```
import Json2Html from 'json-pretty-html'
...
    render(){
    ...
        let dataDom = h('p', {
            className: css.note,
            dangerouslySetInnerHTML: {
                __html: Json2Html(that.state.xobj)
            }
        })
...
```
注意__html一定要嵌套才行

---
###致力于让一切变得简单
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END