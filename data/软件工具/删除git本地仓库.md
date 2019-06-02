遇到fatal: destination path '.' already exists and is not an empty directory. 错误是指当前文件夹下已经存在git仓库，需要把旧的仓库删掉。

.git是个隐藏文件，需要
`ls -a`
才能显示，然后
`rm -rf .git`
就可以干掉它了
然后往上一层再
`rm -rf foldername`
就干净了。