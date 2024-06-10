import datetime

tz_utc_8 = datetime.timezone(datetime.timedelta(hours=8))

# 获取当前时间的标准时间格式: 2021-07-22 17:00:00
def getNowDateTime():
    nowTime = datetime.datetime.now(tz=tz_utc_8).strftime("%Y-%m-%d %H:%M:%S")
    return nowTime


# 获取当前时间的节点格式: 17:00
def getNowTime():
    nowTime = datetime.datetime.now(tz=tz_utc_8).strftime("%H:%M")
    return nowTime


# 将时间字符串转换为时间戳
def getTimeStamp(dataTimeStr):
    d = datetime.datetime.strptime(dataTimeStr, "%Y-%m-%d %H:%M:%S")
    t = int(d.timestamp())
    return t


# 将时间戳转换为时间字符串
def getDateTimeStr(timeStamp):
    d = datetime.datetime.fromtimestamp(timeStamp, tz=tz_utc_8)
    f = d.strftime("%Y-%m-%d %H:%M:%S")
    return f


# 获取当前时间的日期格式: 2021_07_22
def getNowDate():
    nowTime = datetime.datetime.now(tz=tz_utc_8).strftime("%Y_%m_%d")
    return nowTime


# 获取格式化的时间戳: 2022_06_10-19_10_32
def getFoarmatTimestamp():
    return datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")


# 获取格式化的纳秒级时间戳
def getFoarmatNanoTimestamp():
    return datetime.datetime.utcnow().strftime("%Y_%m_%d-%H_%M_%S_%f")[:-3]


# 将日期字符串转换为指定格式
def convertDataFormat(text):
    try:
        srcTime = datetime.datetime.strptime(text, "%Y-%m-%d")
        return srcTime.strftime("%Y_%m_%d")
    except ValueError:
        print("文件名的日期格式有误，请检查", text)
    return ""


# 将UTC-0时间字符串转换为UTC+8时间
def get_datatime_utc_8(utc_0_iso):
    t = datetime.datetime.fromisoformat(utc_0_iso)
    local_dt = t.astimezone(tz_utc_8)
    return local_dt


# 获取datetime字符串
def get_datatime_str(dt):
    return datetime.datetime.strftime(dt, "%Y-%m-%d %H:%M:%S")


# 获取当前时间的ISO格式字符串
def get_now_iso_time(dt=datetime.datetime.now(tz_utc_8)):
    d = dt.isoformat()
    return d


# 排序日期列表
def sort_by_date(date_list):
    date_list.sort(key=lambda x: x[0])
    return date_list


# 格式化日期列表
def format_date(date_list):
    return [date.strftime("%Y-%m-%d") for date in date_list]


# 获取指定间隔的日期列表
def get_date_list(start_date, end_date, delta_days):
    date_list = []
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    delta = datetime.timedelta(days=delta_days)
    while start_date <= end_date:
        date_list.append(start_date)
        start_date += delta
    return date_list


# 获取不同间隔的日期列表
def get_date_list_by_month(start_date, end_date):
    return get_date_list(start_date, end_date, 31)


def get_date_list_by_year(start_date, end_date):
    return get_date_list(start_date, end_date, 365)


def get_date_list_by_quarter(start_date, end_date):
    return get_date_list(start_date, end_date, 91)


def get_date_list_by_half_year(start_date, end_date):
    return get_date_list(start_date, end_date, 182)


def get_date_list_by_year_and_quarter(start_date, end_date):
    return get_date_list(start_date, end_date, 91)


def get_date_list_by_year_and_half_year(start_date, end_date):
    return get_date_list(start_date, end_date, 182)


def get_date_list_by_year_and_month(start_date, end_date):
    return get_date_list(start_date, end_date, 30)


def get_date_list_by_month_and_day(start_date, end_date):
    return get_date_list(start_date, end_date, 1)
