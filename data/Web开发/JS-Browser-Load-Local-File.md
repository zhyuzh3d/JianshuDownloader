浏览器端怎么载入本地文件？

* 首先要创造一个input元素，click它触发选择文件的弹窗
* 然后给它一个监听，选择文件change的时候执行触发动作
* 触发动作使用FileReader读取文件，再触发读取成功后的内容操作

主要代码
```
let file_input = document.createElement('input')
        file_input.setAttribute('accept', ".mdr")
        file_input.addEventListener("change", (evt) => {
            let f = evt.target.files ? evt.target.files[0] : null
            if (!f) return
            var reader = new FileReader()
            reader.onload = function (e) {
                var contents = e.target.result
                var xobj = null
                try {
                    xobj = JSON.parse(contents)
                    console.log('xobj', xobj)
                } catch (err) {
                    console.log('>LoadRules:ERR:', err.message)
                }
                if (xobj) {
                    that.setState({
                        xobj: xobj
                    })
                }            
            }
            reader.readAsText(f);
        }, false)
        file_input.type = 'file'
        file_input.click()
```
>注意，虽然设置了accept属性限定文件类型，但有时候没有作用
JSON.parse可能异常，需要做try捕捉

---
###致力于让一切变得简单
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END