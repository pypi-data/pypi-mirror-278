"""
datetime对象
    创建方法:
        now
        strptime
    int属性相关方法：
        year eg: 2023 eg: 2023
        month [1-12] eg: 11
        day [1-31] eg: 3
        hour [0-23] eg: 15
        minute [0-59] eg: 23
        second [0-59] eg: 29
        microsecond <class 'int'> eg: 761715
    对象属性相关方法：
        tzinfo <class 'pytz.tzfile.Asia/Shanghai'> cur_tzinfo: Asia/Shanghai
        date <class 'datetime.date'> cur_date: 2023-11-03
        time <class 'datetime.time'> cur_time: 15:20:10.914473
        date.time_tuple <class 'time.struct_time'>
            tm_wday：一周中的一天，0 (星期一) 到 6 (星期日)
            tm_yday：一年中的第几天，1 到 366
            tm_isdst：夏令时，值为 -1, 0, 1, 其中 -1 表示未知
            week_number: 今年的第{}周
    字符串相关方法：
        strftime: datetime -> str <class 'str'> cur_strftime: 2023-11-03 15:20:10
        strptime: str -> datetime <class 'datetime.datetime'> cur_datetime: 2023-11-03 15:20:10
timedelta对象
    属性
        days：返回该 timedelta 对象表示的总天数。值可以是正数或负数。
        seconds：返回该 timedelta 对象表示的秒数（不包括天数转换的秒数）。这个值总是在0到86399之间（包含两端的值）。
        microseconds：返回该 timedelta 对象表示的微秒数（不包括天数或秒数转换的微秒数）。这个值总是在0到999999之间（包含两端的值）。
    方法
        total_seconds()：返回 timedelta 对象表示的总秒数（包括天数、小时、分钟转换的秒数），结果是一个浮点数。
    构造方法
        # 创建一个代表1天2小时3分钟4秒的timedelta对象
        td = timedelta(days=1, hours=2, minutes=3, seconds=4)
    测试方法
        print(td.days)  # 输出：1
        print(td.seconds)  # 输出：7384，即2小时3分钟4秒转换为秒的结果
        print(td.microseconds)  # 输出：0，因为我们没有指定微秒数
        print(td.total_seconds())  # 输出：97204.0，即1天2小时3分钟4秒转换为秒的结果
"""

from datetime import datetime, timedelta
from pytz import timezone
import calendar
import time
import moment
import inspect
from fish_util.src.loguru_util import (
    default_logger,
    print,
    debug,
    info,
    warning,
    error,
    critical,
    cat,
    catcher,
)


date_format = "%Y-%m-%d"
time_format = "%H:%M:%S"
datetime_format = "%Y-%m-%d %H:%M:%S"
full_datetime_format = "%Y-%m-%d %H:%M:%S.%f"
str_shanghai = "Asia/Shanghai"
cur_tz = timezone(str_shanghai)


class MomentUtil:
    # 获取一个datetime对象，不传参数则获取当前时间
    @staticmethod
    def new_datetime(datetime_str=None):
        if datetime_str is None:
            return datetime.now(cur_tz)
        return datetime.strptime(datetime_str, datetime_format)

    # 1698999480.283332
    @staticmethod
    def to_timestamp(dt=None):
        if dt is None:
            dt = MomentUtil.new_datetime()
        return dt.timestamp()

    @staticmethod
    def from_timestamp(timestamp):
        return datetime.fromtimestamp(timestamp)

    # 2023-11-03 16:18:00
    @staticmethod
    def to_str(dt=None, format=datetime_format):
        if dt is None:
            dt = MomentUtil.new_datetime()
        return dt.strftime(format)

    @staticmethod
    def from_str(datetime_str, format=date_format):
        return datetime.strptime(datetime_str, format)

    # 2023-11-03
    @staticmethod
    def get_day_str(dt=None, format=date_format):
        return MomentUtil.to_str(dt, format)

    # 16:18:00
    @staticmethod
    def get_time_str(dt=None, format=time_format):
        return MomentUtil.to_str(dt, format)

    # (2023, 11, 3, 17, 36, 16, 344218, 1699004176.344218)
    @staticmethod
    def get_values(dt=None):
        if dt is None:
            dt = MomentUtil.new_datetime()
        year = dt.year  # 年份，范围是 1 到 9999。
        month = dt.month  # 月份，范围是 1 到 12。
        day = (
            dt.day
        )  # 一个月中的哪一天，范围是 1 到 31（对于普通月份）或 1 到 32（对于闰年）
        hour = dt.hour  # 小时，范围是 0 到 23。
        minute = dt.minute  # 分钟，范围是 0 到 59。
        second = dt.second  # 秒，范围是 0 到 59。
        microsecond = dt.microsecond  # 微秒，范围是 0 到 999999。
        timestamp = (
            dt.timestamp()
        )  # <class 'float'> timestamp: 1699001072.214729 整数为秒，小数为微秒
        # cat(year,month,day,hour,minute,second,microsecond,timestamp)
        return year, month, day, hour, minute, second, microsecond, timestamp

    # 1699001072 单位：秒
    @staticmethod
    def get_timestamp(dt=None):
        return int(MomentUtil.get_values(dt)[-1])

    # diff=dt2-dt1
    # (days,seconds,microseconds,total_seconds)
    # (11229, 33491, 292470, 970219091.29247)
    # 970219091=33491+11229*24*3600
    @staticmethod
    def get_diff(dt2, dt1):
        diff = dt2 - dt1
        days = diff.days
        seconds = diff.seconds
        microseconds = diff.microseconds
        total_seconds = diff.total_seconds()
        cat(diff)  # 输出：9:30:00
        cat(days, seconds, microseconds, total_seconds)
        return days, seconds, microseconds, total_seconds

    @staticmethod
    def get_basic_offset(dt=None):
        if dt is None:
            dt = MomentUtil.new_datetime()
        cur_timetuple = dt.timetuple()
        week_day = (
            cur_timetuple.tm_wday
        )  # <class 'int'> 一周中的哪一天，范围是 0（星期一）到 6（星期日）。
        year_day = (
            cur_timetuple.tm_yday
        )  # <class 'int'> 一年中的哪一天，范围是 1 到 366。
        year_week = dt.isocalendar()[
            1
        ]  # <class 'int'> 每年的第几周，范围是 1 到 53（53 周是最后一周，没有第 54 周）。
        cat(week_day, year_day, year_week)
        return week_day, year_day, year_week


# 直接运行时
@catcher
def main():
    print(f"[run main: {__file__}]")
    # 创建一个datetime对象
    dt = MomentUtil.new_datetime()
    cat(dt)
    print("----------[obj]-------------")
    cur_tzinfo = dt.tzinfo
    cur_date = dt.date()
    cur_time = dt.time()
    cur_timetuple = dt.timetuple()
    cur_calendar = dt.isocalendar()
    cat(cur_tzinfo, cur_date, cur_time, cur_timetuple, cur_calendar)
    print("----------[int]-------------")
    get_second = MomentUtil.get_values(dt)
    cat(get_second)
    print("----------[str]-------------")
    cur_strftime = MomentUtil.to_str(
        dt
    )  # <class 'str'> cur_strftime: 2023-11-03 16:35:42
    cur_strftime_full = MomentUtil.to_str(
        dt, full_datetime_format
    )  # <class 'str'> cur_strftime_full: 2023-11-03 16:35:42.499331
    cur_date = MomentUtil.get_day_str(dt)
    cur_time = MomentUtil.get_time_str(dt)
    cat(cur_strftime, cur_strftime_full, cur_date, cur_time)
    print("----------[基本日期计算]-------------")
    basic_offset = MomentUtil.get_basic_offset(dt)
    cat(basic_offset)
    print("----------[计算两个日期之间的天数]-------------")
    date1 = datetime(2023, 11, 3)
    date2 = datetime(2023, 12, 25)
    diff = MomentUtil.get_diff(date2, date1)
    print(diff[0])  # 输出：52
    print("----------[添加或减少时间]-------------")
    date = datetime.now()
    date_plus_10days = date + timedelta(days=10)
    date_minus_10days = date - timedelta(days=10)
    print("Today:", date)
    print("10 days from now:", date_plus_10days)
    print("10 days ago:", date_minus_10days)
    print(f"----------[计算两个时间点之间的时间差]----------")
    time1 = datetime(1993, 2, 4, 8, 12, 23, 123456)  # 1993-02-04 8:12:23 AM
    time2 = datetime(2023, 11, 3, 17, 30, 34, 415926)  # 2023-11-03 5:30:34 PM
    diff = MomentUtil.get_diff(time2, time1)
    print(diff)
    print(f"----------[获取指定日期所在周的第一天和最后一天]----------")
    # 假设我们指定的日期是2023年11月3日
    date = datetime(2023, 11, 3)
    # 在Python中，weekday()函数返回的是一个整数，表示这一天是一周中的第几天，周一是0，周二是1，以此类推，周日是6
    # 所以我们可以通过减去weekday()的结果来得到周一的日期
    start_of_week = date - timedelta(days=date.weekday())
    # 然后我们可以通过加上6来得到周日的日期
    end_of_week = start_of_week + timedelta(days=6)
    print(start_of_week)  # 输出：2023-10-30 00:00:00，这是周一的日期
    print(end_of_week)  # 输出：2023-11-05 00:00:00，这是周日的日期


# 外部导入时,主要是被import
@catcher
def launch():
    print(f"run launch: {__file__}")


if __name__ == "__main__":
    main()
    print("[end main]")
else:
    launch()
    print("[end launch]")
