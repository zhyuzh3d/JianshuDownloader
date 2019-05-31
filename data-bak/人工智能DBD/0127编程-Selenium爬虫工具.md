>[点击这里进入**人工智能DBD嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---

Selenium主要包含：
- Webdriver，各种浏览器驱动软件，用来控制浏览器的。
- API，各种编程语言可以调用的模块，代码通过它衔接Webdriver进而控制浏览器。
- Server，服务程序，如果你需要远程控制其他电脑上的代码和Webdriver，就要在那些电脑上装这个服务程序。
- IDE，浏览器插件，有界面，快速方便的执行简单测试，[参考这里](https://www.jianshu.com/p/2f512d43cf60)。

大多数情况下，我们只要Webdriver和API就够了。

## Python安装环境

- 先下载对应浏览器的Webdriver。[谷歌Chrome浏览器点这里](https://sites.google.com/a/chromium.org/chromedriver/downloads),注意你的Chrome应该升级到70版本以上，下载后无需安装，放在固定的目录就好。

- 安装API，使用命令`conda install -c conda-forge selenium`或者pip直接装，有些慢，多等等。

安装成功之后，测试以下代码，顺利弹出浏览器打开百度的话就成功了。
```
from selenium import webdriver
driver = webdriver.Chrome('/Applications/chromedriver')
driver.get("http://www.baidu.com")
```

## 页面元素提取

先看一下代码：
```
from selenium import webdriver
from selenium.webdriver.common.by import By
driver = webdriver.Chrome('/Applications/chromedriver') #替换为你的chromdriver拷贝的目录
driver.get("https://su.58.com/zufang/pn2/?PGTID=0d300008-0000-5965-8ce1-1873463f7758&ClickID=1")
litag=driver.find_element(By.CLASS_NAME,'listUl')
li=litag.find_elements(By.TAG_NAME,'li')
len(li)
li[3].text
```
这里直接从driver中`find_element`，参数`(By.CLASS_NAME,'listUl')`是通过class名来搜索单个元素，相应的`find_elements`则是搜索多个元素。

除了`By. CLASS_NAME`还可以:
-  `(by=By.ID, value=tagid")`
- `(By.TAG_NAME, "div")`
- `(By.NAME, "tagnameAttr")`
- `(By.LINK_TEXT, "点击这里查看详情")`
- `(By.PARTIAL_LINK_TEXT, "详情")`
- `(By.CSS_SELECTOR, "#food span.dairy.aged")`
- `(By.XPATH, "//input")`

>官方默认并没有提供通过任意属性获得元素的方法，这种问题只能通过xpath来实现，比如`driver.find_element(By.XPATH,'//ul[@class="listUl"]')`可以提取class属性为listUI的ul标记元素。

除了直接从html中提取，还可以用js代码提取：
`driver.execute_script("return $('.cheese')[0]") #对于使用jquery的页面` 

甚至可以传递参数进去，下面这个命令直接在浏览器中弹窗：
```
msg = 'Hello Selenium！'
driver.execute_script('''
    alert(arguments[0])
''', msg)
```

##控制页面交互

- send_key向输入框中添加文字，`inputElement.send_keys("cheese!")`
- submit提交表单，`inputElement.submit()`
- click点击按钮,`btnElement.click()`

选择选项：
```
from selenium.webdriver.support.ui import Select
select = Select(driver.find_element_by_tag_name("select"))
select.deselect_all()
select.select_by_visible_text("Edam")
```

切换浏览器选项卡:
```python
for handle in driver.window_handles:
    driver.switch_to.window(handle)
```

切换到弹窗:
```
alert = driver.switch_to.alert #alert.dismiss()
```
前进后退
```python
driver.forward()
driver.back()
```

Cookie操作:
```
driver.get("http://www.example.com")
driver.add_cookie({'name':'key', 'value':'value', 'path':'/'})L
for cookie in driver.get_cookies():
    print "%s -> %s" % (cookie['name'], cookie['value'])
driver.delete_cookie("CookieName")
driver.delete_all_cookies()
```

拖拽实现：
```
from selenium.webdriver.common.action_chains import ActionChains
element = driver.find_element_by_name("source")
target =  driver.find_element_by_name("target")

ActionChains(driver).drag_and_drop(element, target).perform()
```

## 等待页面加载

Selenium并没有直接页面ready的回调，但提供了对任意元素状态的监听：
```
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

browser = webdriver.Firefox()
browser.get("url")
delay = 3 #最多等3秒
try:
    elem=EC.presence_of_element_located((By.ID, 'IdOfMyElement'))
    myElem = WebDriverWait(browser, delay).until(elem)
    print "Element is ready!"
except TimeoutException:
    print "Loading took too much time!"
```
`expected_conditions`不仅提供了元素是否存在`presence_of_element_located`的监听，而且可以检测元素是否可用、是否显示、是否可点击等多种情况。

##更多资料
[ChromeDriver官方参考](https://seleniumhq.github.io/selenium/docs/api/java/org/openqa/selenium/chrome/ChromeDriver.html)
[Selenium官方参考](https://www.seleniumhq.org/docs/03_webdriver.jsp)

>Selenium最强大的地方在于它直接控制浏览器，也就是，只要在浏览器中最终展示的数据都可以通过Selenium得到，无论是html还是js后续填充的内容。当然Selenium缺点就是经常浪费了浏览器的渲染时间，毕竟我们要的是数据而不是浏览器画面。

---
>[点击这里进入**人工智能DBD嘚吧嘚**目录，观看全部文章](https://www.jianshu.com/p/ff37dbc75edb)
---
###每个人的智能新时代
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得很有用，欢迎转载~
---
END