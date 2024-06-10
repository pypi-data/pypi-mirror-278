from datetime import datetime, timedelta, timezone

tz_utc_8 = timezone(timedelta(hours=8))


# 创建UTC+8北京时间的datetime的标准时间格式,eg: 2021-06-15 16:30:38
def get_now_date_time():
    tz_utc_8 = timezone(timedelta(hours=8))
    now_time = datetime.now(tz=tz_utc_8).strftime("%Y-%m-%d %H:%M:%S")
    return now_time


# 方便生成Logseq可以识别的日志文件格式，eg: 2021_06_15
def get_now_date():
    tz_utc_8 = timezone(timedelta(hours=8))
    now_time = datetime.now(tz=tz_utc_8).strftime("%Y_%m_%d")
    return now_time


# 方便生成Obsidian-Memos可以识别的节点格式,eg: 16:30
def get_now_time():
    tz_utc_8 = timezone(timedelta(hours=8))
    now_time = datetime.now(tz=tz_utc_8).strftime("%H:%M")
    return now_time


# str  -> timeStamp,eg: 1696814438
def get_time_stamp(date_time_str):
    d = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
    t = int(d.timestamp())
    return t


# timeStamp  -> str,eg: 2021-06-15 16:30:38
def get_time_str(time_stamp):
    last_time = 1664092451
    d = datetime.fromtimestamp(time_stamp, tz=tz_utc_8)
    f = d.strftime("%Y-%m-%d %H:%M:%S")
    return f


def test():
    print(__file__)
    now_date_time = get_now_date_time()
    now_date = get_now_date()
    now_time = get_now_time()
    time_stamp = get_time_stamp(now_date_time)
    time_str = get_time_str(time_stamp)
    print("now_date_time: ", now_date_time)
    print("now_date: ", now_date)
    print("now_time: ", now_time)
    print("time_stamp: ", time_stamp)
    print("time_str: ", time_str)


if __name__ == "__main__":
    test()
