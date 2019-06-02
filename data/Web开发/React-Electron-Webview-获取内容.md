如何在其他元素内获取webview载入的guest内容？

###问题点在于：
* 在主进程中如何获得渲染进程中的内容
* webview是客体内容，如何跨越到其他元素的渲染进程内
* 获得webview的webContent似乎并没有什么用，只和事件有关，和内容无关
* 即使获得了内容，但不一定能正常转为Dom进行query查询

###解决方案：
1. 在创建webview的时候添加dom-ready监听，完成内容加载后触发
1. 使用dom的executeJavaScript('code',callback(result))方法提取出webview的内部文字
1. 利用createDocumentFragment方法创造片段，再createElement创建html元素，把元素放入到片段中，使其可以query查询

###实际代码
```
componentDidMount() {
        let that = this
        //将webview内容同步到编辑窗口
        const browser = document.querySelector('webview')
        browser.addEventListener('dom-ready', (e) => {
            browser.executeJavaScript(`document.documentElement.innerHTML`, function (str) {
                that.setState({
                    docStr: str
                })

                let doc = document.createDocumentFragment()
                let el = document.createElement('html')
                el.innerHTML = str
                doc.appendChild(el)
                var text = doc.querySelector('head').innerHTML
                console.log('>>>head', $(doc).find('head title').html())
                console.log('>>>body', $(doc).find('body').html())
            })
        })
    }

```
>注意点：
webview.getWebContent方法拿到webContent，但根本没卵用；
直接$(str)会导致无法查询head里面的元素，拿不到title等信息；


---
###致力于让一切变得简单
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END