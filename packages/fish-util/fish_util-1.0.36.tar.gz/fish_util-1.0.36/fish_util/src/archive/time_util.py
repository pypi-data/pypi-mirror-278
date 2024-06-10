# [Python3 日期和时间 | 菜鸟教程](https: // www.runoob.com/python3/python3-date-time.html)
#!/usr/bin/python3
"""
python中时间日期格式化符号：
%y 两位数的年份表示（00-99）
%Y 四位数的年份表示（000-9999）
%m 月份（01-12）
%d 月内中的一天（0-31）
%H 24小时制小时数（0-23）
%I 12小时制小时数（01-12）
%M 分钟数（00=59）
%S 秒（00-59）
%a 本地简化星期名称
%A 本地完整星期名称
%b 本地简化的月份名称
%B 本地完整的月份名称
%c 本地相应的日期表示和时间表示
%j 年内的一天（001-366）
%p 本地A.M.或P.M.的等价符
%U 一年中的星期数（00-53）星期天为星期的开始
%w 星期（0-6），星期天为星期的开始
%W 一年中的星期数（00-53）星期一为星期的开始
%x 本地相应的日期表示
%X 本地相应的时间表示
%Z 当前时区的名称
%% %号本身
"""

from datetime import datetime
import moment
import calendar
import time  # 引入time模块


def now_timestamp():
    return int(time.time()*1000)


# v = now_timestamp()
# print(v)


def main(param):
    print(f"{__file__} main")
    print(f"param: {param}")
    if param != "test":
        return
    ticks = time.time()
    print("当前时间戳为:", ticks)

    localtime = time.localtime(time.time())
    print("本地时间为 :", localtime)

    localtime = time.asctime(time.localtime(time.time()))
    print("本地时间为 :", localtime)

    # 格式化成2016-03-20 11:45:39形式
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    # 格式化成Sat Mar 28 22:24:24 2016形式
    print(time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()))

    # 将格式字符串转换为时间戳
    a = "Sat Mar 28 22:24:24 2016"
    print(time.mktime(time.strptime(a, "%a %b %d %H:%M:%S %Y")))

    cal = calendar.month(2016, 1)
    print("以下输出2016年1月份的日历:")
    print(cal)

    # Create a moment from a string
    moment.date("12-18-2012")

    # Create a moment with a specified strftime format
    moment.date("12-18-2012", "%m-%d-%Y")

    # Moment uses the awesome dateparser library behind the scenes
    moment.date("2012-12-18")

    # Create a moment with words in it
    moment.date("December 18, 2012")

    # Create a moment that would normally be pretty hard to do
    moment.date("2 weeks ago")

    # Create a future moment that would otherwise be really difficult
    moment.date("2 weeks from now")

    # Create a moment from the current datetime
    moment.now()

    # The moment can also be UTC-based
    moment.utcnow()

    # Create a moment with the UTC time zone
    moment.utc("2012-12-18")

    # Create a moment from a Unix timestamp
    moment.unix(1355875153626)

    # Create a moment from a Unix UTC timestamp
    moment.unix(1355875153626, utc=True)

    # Return a datetime instance
    moment.date(2012, 12, 18).date

    # We can do the same thing with the UTC method
    moment.utc(2012, 12, 18).date

    # Create and format a moment using Moment.js semantics
    moment.now().format("YYYY-M-D")

    # Create and format a moment with strftime semantics
    moment.date(2012, 12, 18).strftime("%Y-%m-%d")

    # Update your moment's time zone
    moment.date(datetime(2012, 12, 18)).locale("US/Central").date

    # Alter the moment's UTC time zone to a different time zone
    moment.utcnow().timezone("US/Eastern").date

    # Set and update your moment's time zone. For instance, I'm on the
    # west coast, but want NYC's current time.
    moment.now().locale("US/Pacific").timezone("US/Eastern")

    # In order to manipulate time zones, a locale must always be set or
    # you must be using UTC.
    moment.utcnow().timezone("US/Eastern").date

    # You can also clone a moment, so the original stays unaltered
    now = moment.utcnow().timezone("Asia/Shanghai")
    print(f"now: {now} type: {type(now)}")

    now_date = now.date
    print(f"now_date: {now_date} type: {type(now_date)}")

    now_time = now_date.timestamp()
    print(f"now_time: {now_time} type: {type(now_time)}")

    now_timestamp = int(now_time*1000)
    print(f"now_timestamp: {now_timestamp} type: {type(now_timestamp)}")

    future = now.clone().add(weeks=2)


if __name__ == '__main__':
    main("test")
