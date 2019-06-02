首先要增加time.h。
```
#include <time.h>
int main(){

}
```
---
##time(NULL)
返回一个time_t类型结果，也可以直接当int处理，是一个10位数字，表示从1970年开始到现在的毫秒数。括号里的NULL不能省略：
```
time_t now=time(NULL);
int nowint=time(NULL);
cout << now;
cout << '\n';
cout << nowint;
```
输出结果：
```
1527856055
1527856055
```
---
##clock()
同样返回一个time_t，也可以当做int，表示从程序启动开始经过了多少毫秒。
```
	time_t pass=clock();
	int passint=clock();
	cout << pass;
	cout << '\n';
	cout << passint;
```
输出结果
```
250
250
```
---
##localtime()
完整语法格式
struct tm * localtime (const time_t * timer)
返回的是一个结构指针，参数是一个time_t的地址。
tm的结构是：
```
struct tm {
  int tm_sec;       /* 秒 – 取值区间为[0,59] */
  int tm_min;       /* 分 - 取值区间为[0,59] */
  int tm_hour;      /* 时 - 取值区间为[0,23] */
  int tm_mday;     /* 一个月中的日期 - 取值区间为[1,31] */
  int tm_mon;     /* 月份（从一月开始，0代表一月） - 取值区间为[0,11] */
  int tm_year;     /* 年份，其值等于实际年份减去1900 */
  int tm_wday;    /* 星期 – 取值区间为[0,6]，其中0代表星期天，1代表星期一 */
  int tm_yday;    /* 从每年1月1日开始的天数– 取值区间[0,365]，其中0代表1月1日 */
  int tm_isdst;    /* 夏令时标识符，夏令时tm_isdst为正；不实行夏令时tm_isdst为0 */
};
```
测试代码：
```
	time_t now=time(NULL);
	struct tm *tm_now;
	tm_now=localtime(&now);
	cout << tm_now->tm_year+1900;
```
>*是指针，&是取地址。->箭头相当于.点,用于指针.属性名。

输出：
```
2018
```

---
###让知识变得简单
如果您发现文章错误，请不吝留言指正；
如果您觉得有用，请点喜欢；
如果您觉得有价值，欢迎转载~
---
END



