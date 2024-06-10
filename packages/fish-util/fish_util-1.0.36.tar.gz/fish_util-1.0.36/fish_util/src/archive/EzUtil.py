import os
import requests
import re
import json
import zipfile
import functools
import time
from datetime import datetime, timezone, timedelta
import pytz

current_year = time.strftime("%Y", time.localtime())
current_month = time.strftime("%Y-%m", time.localtime())
current_day = time.strftime("%Y-%m-%d", time.localtime())
current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

CACHE = "/Users/yutianran/Documents/MyObsidian/Attachment/Cache"

# 打包目录为zip文件（未压缩）
def make_zip(source_dir):
    out_dir = os.path.split(source_dir)[0]
    out_name = os.path.split(source_dir)[1]+".zip"
    output_filename = path = os.path.join(out_dir, out_name)
    print(f"打包文件夹：{source_dir} -> {output_filename}")
    zipf = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
            zipf.write(pathfile, arcname)
    zipf.close()

# 根据生成的mapping文件来执行重命名
def exeute_rename_by_mapping(mapping):
    mdict = read_map(mapping)
    # 执行之前先压缩文件夹做备份
    p = list(mdict.values())[0]
    d = os.path.split(p)[0]
    make_zip(d)
    for key, value in mdict.items():
        print(f"{key} -> {value}")
        os.rename(key, value)
    print(f"执行mapping重命名成功：{mapping}")

# 返回用来排序的指标，如果没有 解读你身边的经济学 (23).md 等则返回0 ，否则就返回23
def get_num(path):
    p = re.compile(r' [(](\d+)[)].md', re.S)
    plist = re.findall(p, path)
    if len(plist) == 0:
        return 0
    else:
        return int(plist[0])


# 获取真实的目录列表，非1-44的这种文件重命名列表
def get_real_content_list(path):
    file = open(path, "r")
    lines = file.readlines()
    content_list = []
    for line in lines:
        # 以“- ”开头的行
        if re.match('^- .*$', line):
            content_list.append(real_strip(line))
    return content_list

# 输出列表
def print_list(val):
    for item in val:
        print(item)

# 按 key -> value 组成列表的一项
def map_to_list(mdict):
    mlist = []
    for key, value in mdict.items():
        mlist.append(f"{key} -> {value}")
    return mlist

# 按 key -> value 组成列表的一项
def map_to_json(mdict):
    mlist = []
    for key, value in mdict.items():
        mlist.append(f"{key} -> {value}")
    return mlist





