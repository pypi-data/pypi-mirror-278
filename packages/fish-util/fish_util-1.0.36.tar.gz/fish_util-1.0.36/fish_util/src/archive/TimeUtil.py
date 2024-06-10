import time
from datetime import datetime

 
# 格式化成2016-03-20 11:45:39形式
# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )
 
# 格式化成Sat Mar 28 22:24:24 2016形式
# print(time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()) )
  
# 将格式字符串转换为时间戳
# a = "Sat Mar 28 22:24:24 2016"
# print(time.mktime(time.strptime(a,"%a %b %d %H:%M:%S %Y")))

# 2022_06_10-19_10_32
def getFoarmatTimestamp():
    return datetime.now().strftime("%Y_%m_%d-%H_%M_%S")

def getFoarmatNanoTimestamp():
    return datetime.utcnow().strftime("%Y_%m_%d-%H_%M_%S_%f")[:-3]

# 日期格式转换 2012-09-20 -> 2012_09_20
def convertDataFormat(text):  
    try:
        srcTime = datetime.strptime(text, '%Y-%m-%d')
        return srcTime.strftime("%Y_%m_%d")
    except ValueError:
        print("文件名的日期格式有误，请检查",text)
        return ""

# 将utc-0的时间转成utc-8的时间
def get_datatime_utc_8(utc_0_iso):
    t = datetime.fromisoformat(utc_0_iso)
    tz_utc_8 = time.timezone(time.timedelta(hours=8))
    local_dt = time.astimezone(tz_utc_8)
    return local_dt

# 获取datetime字符串
def get_datatime_str(dt):
    return datetime.strftime(dt, '%Y-%m-%d %H:%M:%S')

def get_now_iso_time():
    tz_utc_8 = time.timezone(time.timedelta(hours=8))
    d = datetime.now(tz_utc_8).isoformat()
    # datetime.now(timezone.utc).isoformat()
    return d

# # import arrow
# n=datetime.now()
# # .astimezone().isoformat()
# # print(arrow.utcnow().isoformat())
# # s=datetime.strftime(n,'%Y-%m-%dT%H:%M:%S+%Z')

# d8=get_datatime_utc_8(d)
# print(datetime.now(timezone.utc).isoformat())

# print(getFoarmatNanoTimestamp())