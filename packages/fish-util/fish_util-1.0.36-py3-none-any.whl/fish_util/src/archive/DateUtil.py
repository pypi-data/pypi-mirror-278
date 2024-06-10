import datetime,time

# 排序
def sort_by_date(date_list):
    date_list.sort(key=lambda x: x[0])
    return date_list

# 格式化日期
def format_date(date_list):
    for i in range(len(date_list)):
        date_list[i][0] = date_list[i][0].strftime('%Y-%m-%d')
    return date_list

# 获取日期列表
def get_date_list(start_date, end_date):
    date_list = []
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    while start_date <= end_date:
        date_list.append(start_date)
        start_date += datetime.timedelta(days=1)
    return date_list

# 获取日期列表
def get_date_list_by_month(start_date, end_date):
    date_list = []
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    while start_date <= end_date:
        date_list.append(start_date)
        start_date = start_date + datetime.timedelta(days=31)
    return date_list

# 获取日期列表
def get_date_list_by_year(start_date, end_date):
    date_list = []
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    while start_date <= end_date:
        date_list.append(start_date)
        start_date = start_date + datetime.timedelta(days=365)
    return date_list

# 获取日期列表
def get_date_list_by_quarter(start_date, end_date):
    date_list = []
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    while start_date <= end_date:
        date_list.append(start_date)
        start_date = start_date + datetime.timedelta(days=91)
    return date_list

# 获取日期列表
def get_date_list_by_half_year(start_date, end_date):
    date_list = []
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    while start_date <= end_date:
        date_list.append(start_date)
        start_date = start_date + datetime.timedelta(days=182)
    return date_list

# 获取日期列表
def get_date_list_by_year_and_quarter(start_date, end_date):
    date_list = []
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    while start_date <= end_date:
        date_list.append(start_date)
        start_date = start_date + datetime.timedelta(days=91)
    return date_list

# 获取日期列表
def get_date_list_by_year_and_half_year(start_date, end_date):
    date_list = []
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    while start_date <= end_date:
        date_list.append(start_date)
        start_date = start_date + datetime.timedelta(days=182)
    return date_list

# 获取日期列表
def get_date_list_by_year_and_month(start_date, end_date):
    date_list = []
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    while start_date <= end_date:
        date_list.append(start_date)
        start_date = start_date + datetime.timedelta(days=30)
    return date_list

# 获取日期列表
def get_date_list_by_month_and_day(start_date, end_date):
    date_list = []
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    while start_date <= end_date:
        date_list.append(start_date)
        start_date = start_date + datetime.timedelta(days=1)
    return date_list

def str_to_timestamp(str_time=None, fmt='%Y-%m-%dT%H:%M:%S.%fZ'):
    if str_time:
        # 零时区
        t = datetime.datetime.strptime(str_time, fmt)
        # 东八区
        t += datetime.timedelta(hours=8)
        return int(time.mktime(t.timetuple()))
    return int(time.time())
 
 
def str_to_timestamp_3(str_time=None, fmt= '%Y-%m-%dT%H:%M:%S.%fZ'):
    if str_time:
        d = datetime.datetime.strptime(str_time, fmt)
        timeStamp = int(time.mktime(d.timetuple())) + 8 * 3600
        return timeStamp



nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')