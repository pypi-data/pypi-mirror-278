from flask import Flask
from flask import Flask, request, jsonify, g
import datetime
import time
from datetime import datetime, timedelta, timezone

tz_utc_8 = timezone(timedelta(hours=8))
import json

from lib import log_util
print=log_util.debug

# 创建UTC+8北京时间的datetime的标准时间格式
def getNowDateTime():
    nowTime = datetime.now(tz=tz_utc_8).strftime("%Y-%m-%d %H:%M:%S")
    return nowTime


# 获取请求的所有数据
def get_request_all_data(request):
    m = {}
    # 基本信息
    m["time"] = getNowDateTime()
    m["method"] = request.method
    m["url"] = request.url
    m["content_type"] = request.headers.get("content_type")
    # 具体参数
    if request.args is not None:
        m["args"] = request.args.to_dict()
    if m["content_type"] is not None:
        if "application/json" in m["content_type"]:
            m["json"] = request.get_json()
        if "application/x-www-form-urlencoded" in m["content_type"]:
            m["form"] = request.form.to_dict()
        if "multipart/form-data" in m["content_type"]:
            m["form"] = request.form.to_dict()
    if request.files is not None:
        m["files"] = str(request.files.to_dict())
        for key in request.files:
            value = request.files.get(key)
    return m


def request_to_curl(request):
    """将 Flask 的 request 对象转换为 curl 命令"""
    cmd = ["curl", "-X", request.method]

    # 处理请求头
    headers = request.headers
    for k, v in headers.items():
        cmd += ["-H", f"{k}: {v}"]

    # 处理请求 URL 和请求数据
    url = request.url
    if request.query_string:
        url += f"?{request.query_string.decode()}"
    data = request.data
    if data:
        cmd += ["--data-binary", data.decode()]

    # 返回转换后的 curl 命令
    return " ".join(cmd + [url])


def on_before_request():
    g.start_time = time.time()
    request_data = get_request_all_data(request)
    request_curl = request_to_curl(request)
    print(f"Request data: {json.dumps(request_data, indent=2, ensure_ascii=False)}")
    # print(f"Request curl: {request_curl}")


def on_after_request(response):
    end_time = time.time()
    elapsed_time = end_time - g.start_time
    print(f"Request {request.method} {request.path} took {elapsed_time:.5f} s")
    length = response.get_json().get("data").get("len")
    print(f"Response data length: {length}")
    if length is not None and length > 5:
        sub_list = response.get_json().get("data").get("list")[:5]
        pretty_json = json.dumps(sub_list, indent=4, sort_keys=True, ensure_ascii=False)
        print(f"Response data sub_list: {pretty_json}")
    else:
        print(f"Response data: {response.get_data().decode('utf-8')}")


def list_wrapper(li):
    return {"list": li, "len": len(li)}


def resp(code):
    if code == 0:
        return real_resp(code=0, msg="成功")
    return resp(code, msg="失败", data={})


def resp(code, msg="成功", data={}):
    return jsonify({"code": code, "message": msg, "data": data})
