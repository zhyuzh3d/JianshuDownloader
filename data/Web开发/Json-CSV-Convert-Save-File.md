如何在前端浏览器把一个json对象保存为Excel可以打开的csv文件？

* 首先需要一个json到csv的转换器，比如json-csv
* 其次要利用浏览器支持的blob对象，并创建虚拟的文件地址url
* 使用open(url)或者把这个地址放到按钮上就可以了

主要代码
```
import Jsoncsv from 'json-csv'

...
    genCSVUrl(data) {
        let that = this
        if (!data || data.length < 1) {
            console.log('>SaveCSV:ERR', 'Nothing to save.')
            return
        }
        let fields = []//这里要找到object的每个字段名才行
        for (let attr in data[0]) {
            fields.push({
                name: attr,
                label: attr,
            })
        }
        Jsoncsv.csvBuffered(data, {
            fields: fields
        }, (err, csv) => {
            if (err) {
                console.log('>SaveCSV:ERR', err.message)
            } else {
                var blob = new Blob(["\ufeff", csv], {//注意这里的\ufeff是关键，否则乱码
                    type: "text/csv;charset=UTF-8"//注意这里的text/csv，否则可能不是下载而是直接浏览器打开
                })
                var csvUrl = URL.createObjectURL(blob)
                that.setState({
                    csvUrl: csvUrl
                })
            }
        })
    }
...
```
>注意new Blob(["\ufeff", csv]...这里的\ufeff，没有它的话中文会乱码，只在下面设置UTF-8是没有用的！
注意type: "text/csv;charset=UTF-8"，如果是text/pain那就会直接被浏览器打开而不会触发下载。
也可以用open(csvUrl)方法在新窗口中打开，一样会引发下载，但是会多一个空的弹窗。

---
###致力于让一切变得简单
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END