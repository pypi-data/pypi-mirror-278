# coding=utf-8
import asyncio
from playwright.async_api import async_playwright
import requests
import json
import uuid
import re
import sys
import os
import random
from colorlog import ColoredFormatter
import logging
from os.path import abspath, dirname, join
from logging import handlers
from datetime import datetime
from datetime import datetime, timedelta, timezone
from playwright.sync_api import sync_playwright

tz_utc_8 = timezone(timedelta(hours=8))

link_re = r"\[(.*)\]\((https?://[^\)\s]+)\)"


# 创建UTC+8北京时间的datetime的标准时间格式
def getNowDateTime():
    nowTime = datetime.now(tz=tz_utc_8).strftime("%Y-%m-%d %H:%M:%S")
    return nowTime


# 方便生成Logseq可以识别的日志文件格式
def getNowDate():
    nowTime = datetime.now(tz=tz_utc_8).strftime("%Y_%m_%d")
    return nowTime


# 方便生成Obsidian-Memos可以识别的节点格式
def getNowTime():
    nowTime = datetime.now(tz=tz_utc_8).strftime("%H:%M")
    return nowTime


# str -> datetime -> timeStamp
def getTimeStamp(dataTimeStr):
    d = datetime.strptime(dataTimeStr, "%Y-%m-%d %H:%M:%S")
    t = int(d.timestamp())
    return t


# timeStamp -> datetime -> str
def getDateTimeStr(timeStamp):
    # print("origin timeStamp: " + str(int(timeStamp)))
    lastTime = 1664092451
    d = datetime.fromtimestamp(timeStamp, tz=tz_utc_8)
    # print("datetime: " + str(d))
    # %Y-%m-%d %H:%M:%S.%f
    f = d.strftime("%Y-%m-%d %H:%M:%S")
    # print("dataTimeStr: " + f)
    return f


# 打印文件路径
def printPath(path):
    print(path)
    print(os.path.dirname(path), ".dir")
    print(os.path.basename(path), ".basename")
    print(os.path.splitext(path)[0], ".stem")
    print(os.path.splitext(path)[1], ".ext")
    print(os.path.splitext(os.path.basename(path))[0])


# 返回带后缀名的文件名,eg:2022-06-15.md
def getFileExt(path):
    return os.path.basename(path)


# 返回文件的后缀名，可能为空，eg:.md
def getFileExt(path):
    return os.path.splitext(path)[1]


# 返回文件所在的文件夹，eg:C:/Users/Administrator/Dropbox/MyGithub/MyPython/2022-06-15下午2_10_05导出葫芦笔记数据
def getFileDir(path):
    return os.path.dirname(path)


# 返回无后缀名的文件名，eg:2022-06-15
def getFileName(path):
    return os.path.splitext(os.path.basename(path))[0]


# 在同一文件夹下的两个文件，重命名
def renameFileInDir(dir, src, dest):
    fileName = os.path.join(dir, src)
    newFileName = os.path.join(dir, dest)
    print(fileName, "->", newFileName)
    os.rename(fileName, newFileName)


# 增量写入
def writeStrAppend(val, path):
    file = open(path, "a", encoding="utf-8")
    file.write(val)
    file.flush()
    file.close()
    print(f"增量写入文本到文件成功：{path}")


# 合并文件
def mergeFile(src, dest):
    print("mergeFile", src, dest)
    s = readFile(src)
    tf = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    content = f"\n\n## MergeFile-{tf}\n\n" + s
    writeStrAppend(content, dest)
    os.remove(src)


# 遍历文件夹
def traverseDir(dir):
    files = os.listdir(dir)
    for file in files:
        if not os.path.isdir(file):
            f = open(f"{dir}/{file}")
            name = os.path.splitext(os.path.basename(file))[0]
            print(name)


# 遍历文件，一行行遍历，读取文本
def readFileWithLines(file):
    str = ""
    iter_f = iter(file)
    for line in iter_f:
        str = str + line
    return str


# 读取文件
def readFile(path):
    str = ""
    with open(path, "r", encoding="utf-8") as f:
        str = f.read()
    print(f"读取文件成功：{path}")
    return str


# 读取json到map
def read_map(path):
    json_str = readFile(path)
    return json.loads(json_str)


# 遍历文件夹,对每个文件都做一种操作
def traverseDirWithProcess(dir, process):
    files = os.listdir(dir)
    if len(files) == 0:
        print("没有需要操作的文件", dir)
        return
    for file in files:
        if not os.path.isdir(file):
            # f = f"{dir}/{file}"
            f = os.path.join(dir, file)
            process(f)


# 写入map到文件,按json格式保存
def writeMap(val, path):
    file = open(path, "w", encoding="utf-8")
    json_str = json.dumps(val, indent=4, ensure_ascii=False, separators=(",", ":"))
    file.write(json_str)
    file.flush()
    file.close()
    print(f"写入map到文件成功：{path}")


# 写入文本到文件
def writeStr(val, path):  # 写入文本到文件
    if os.path.exists(path):
        os.remove(path)
    with open(path, "w", encoding="utf-8") as file:
        file.write(val)
        print(f"写入文本到文件成功：{path}")


# 增量写入文本到文件
def writeStrAppend(val, path):
    file = open(path, "a", encoding="utf-8")
    file.write(val)
    file.flush()
    file.close()
    print(f"增量写入文本到文件成功：{path}")


# 增量写入文本到文件-在头部添加
def writeStrAppendHead(val, path):
    src = ""
    if os.path.exists(path):
        src = read_file(path)
    file = open(path, "w")
    content = val + "\n" + src
    file.write(content)
    file.flush()
    file.close()
    print(f"增量写入文本到文件头部成功：{path}")


# 写入列表到文件
def writeList(val, path):
    file = open(path, "w")
    file.write("\n".join(val))
    file.flush()
    file.close()
    print(f"写入列表到文件成功：{path}")


# 过滤掉Mac系统默认的.DS_Store文件
def isnotDsStore(val):
    if not re.match("^.*[.]DS_Store$", val):
        return True
    else:
        return False


def traverseFolder(dirPath, process):
    # 获取目录列表
    listDir = os.listdir(dirPath)
    # 遍历目录列表
    for path in listDir:
        fullPath = os.path.join(dirPath, path)
        # 是文件夹的话，就先打印文件夹的名称，再去遍历这个子文件夹
        if os.path.isdir(fullPath):
            # print(fullPath)
            traverseFolder(fullPath, process)
        # 是文件的话，直接处理就好了
        else:
            process(fullPath)


def delete(path):
    end = path[-7:]
    # print(path)
    li = ["(1).pdf", "(2).pdf", "(1).mp3", "(2).mp3"]
    if end in li:
        # os.remove(path)
        print(path)


# import traceback


# 打印函数Frame MyLogUtil.py:167 f1()
def formatFrameStr(frame):
    funcName = frame.f_code.co_name
    filePath = frame.f_code.co_filename
    fileName = os.path.basename(filePath)
    fileLineno = frame.f_lineno
    return f"{fileName}:{fileLineno} {funcName}()"


# 打印被装饰的函数Frame MyLogUtil.py:167 f1()->f2()
def formatAnnoFrameStr(frame):
    funcName = frame.f_code.co_name
    filePath = frame.f_code.co_filename
    fileName = os.path.basename(filePath)
    fileLineno = frame.f_lineno
    return f"{fileName}:{fileLineno} {funcName}()"


# 打印所有函数Frame depth=回溯深度，无则回溯到最底层
def getFrames(depth=float("inf")):
    # print(f"depth: {depth}")
    trace = sys._getframe(0)
    str = formatFrameStr(trace)
    printDepth = 0
    while trace.f_back and printDepth <= depth:
        str = formatFrameStr(trace.f_back)
        # logger.debug(f"{printDepth} {str}")
        trace = trace.f_back
        printDepth = printDepth + 1
        # print(f"{printDepth} < {depth}")
    return str


# 获取对象
def get_logger():
    # 配置输出路径 /Users/yutianran/Documents/MyPKM/log/LogUtil_2022_06_15.log
    projectDir = dirname(abspath(__file__))
    logDir = projectDir + "/log"
    date = getNowDate()
    logPath = join(logDir, f"LogUtil_{date}.log")
    debugLogPath = join(logDir, f"DebugLog_{date}.log")
    infoLogPath = join(logDir, f"InfoLog_{date}.log")
    errorLogPath = join(logDir, f"ErrorLog_{date}.log")
    # [常见日志参数](https://www.cnblogs.com/nancyzhu/p/8551506.html ) %(funcName)s %(filename)s:%(lineno)d
    logformat = "[%(levelname)-1.1s] %(asctime)s | %(message)s"
    # colorLogformat = "%(log_color)s[%(levelname)1.1s] %(asctime)s | %(message)s"
    LOG_LEVEL = logging.DEBUG
    logging.root.setLevel(LOG_LEVEL)
    # 设置控制台输出
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(LOG_LEVEL)
    streamHandler.setFormatter(
        logging.Formatter(logformat, datefmt="%Y-%m-%d %H:%M:%S")
    )

    # 创建不同级别的文件处理器
    # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，
    # when是间隔的时间单位，单位有以下几种：S-秒 M-分 H-小时 D-天 W-每星期 interval==0时代表星期一 midnight-每天凌晨
    debugFileHandler = handlers.TimedRotatingFileHandler(
        filename=join(logDir, f"LogUtil_{date}_debug.log"),
        when="D",
        backupCount=5,
        encoding="utf-8",
    )
    debugFileHandler.setLevel(logging.DEBUG)
    debugFileHandler.setFormatter(
        logging.Formatter(logformat, datefmt="%Y-%m-%d %H:%M:%S")
    )

    infoFileHandler = handlers.TimedRotatingFileHandler(
        filename=join(logDir, f"LogUtil_{date}_info.log"),
        when="D",
        backupCount=5,
        encoding="utf-8",
    )
    infoFileHandler.setLevel(logging.INFO)
    infoFileHandler.setFormatter(
        logging.Formatter(logformat, datefmt="%Y-%m-%d %H:%M:%S")
    )

    errorFileHandler = handlers.TimedRotatingFileHandler(
        filename=join(logDir, f"LogUtil_{date}_error.log"),
        when="D",
        backupCount=5,
        encoding="utf-8",
    )
    errorFileHandler.setLevel(logging.ERROR)
    errorFileHandler.setFormatter(
        logging.Formatter(logformat, datefmt="%Y-%m-%d %H:%M:%S")
    )

    # 最终创建的Logger对象
    logger = logging.getLogger(logPath)
    logger.setLevel(LOG_LEVEL)
    logger.addHandler(debugFileHandler)
    logger.addHandler(infoFileHandler)
    logger.addHandler(errorFileHandler)
    logger.addHandler(streamHandler)
    return logger


logger = get_logger()


# 给msg加上文件名和行号的装饰器
def formartMsg(msg, depth=0):
    # 为-1时就不加前缀了
    if depth == -1:
        return msg
    prefix = getFrames(depth)
    msg = f"{prefix} | {msg}"
    return msg


# 默然日志方法，方便替换级别
def log(msg, depth=2):
    logger.info(formartMsg(msg, depth))


# 用装饰器，修改msg为formatMsg
def msgWrapper(func):
    def wrapper(*args, **kwargs):
        msg = args[0]
        foarmatMsg = formartMsg(msg, 2)
        # print(f"msg: {msg}")
        # print(f"foarmatMsg: {foarmatMsg}")
        func(foarmatMsg, **kwargs)

    return wrapper


# 封装几个简单的方法，以供外界调用
# 调试信息
# 主要有装饰器自动添加的参数打印
def debug(msg, depth=2):
    logger.debug(formartMsg(msg, depth))


# 日常开发信息-默认
@msgWrapper
def info(msg):
    logger.info(msg)


# 重要警告信息
@msgWrapper
def warning(msg):
    logger.warning(msg)


# 错误信息
@msgWrapper
def error(msg):
    logger.error(msg)


@msgWrapper
def critical(msg):
    logger.critical(msg)


# 替换常用的print为LogUtil
print = debug
printf = debug


def test_log():
    debug("This is debug.")
    info("This is info.")
    warning("This is warning.")
    error("This is error.")
    critical("This is critical.")
    log("This is log.")


def read_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file '{filename}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


# 正则表达式用于查找文件中没有http的行
def find_lines_without_regex(content):
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if not re.search(link_re, line):
            print(f"Line {i+1}: {line.strip()}")


# 正则表达式用于查找Markdown中的链接
def find_md_links(md_content):
    links = re.findall(link_re, md_content)
    return links


def save_url(url):
    api = "https://api-prod.omnivore.app/api/graphql"
    url_uuid = uuid.uuid5(uuid.NAMESPACE_URL, url)
    payload = json.dumps(
        {
            "query": "mutation SaveUrl($input: SaveUrlInput!) { saveUrl(input: $input) { ... on SaveSuccess { url clientRequestId } ... on SaveError { errorCodes message } } }",
            "variables": {
                "input": {
                    "clientRequestId": str(url_uuid),
                    "source": "api",
                    "url": url,
                }
            },
        }
    )
    headers = {
        "authorization": "5453e79e-0b85-44e2-9827-fb5476ab1c7c",
        "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
        "content-type": "application/json",
        "Accept": "*/*",
        "Host": "api-prod.omnivore.app",
        "Connection": "keep-alive",
    }
    response = requests.request("POST", api, headers=headers, data=payload)
    print(response.status_code, response.text)


def get_real_url(url):
    random_ip = random.choice(ips)
    ip = random_ip.get("ip")
    port = random_ip.get("port")
    print(f"url: {url} random_ip: {ip}:{port}")
    # 初始化Playwright
    with sync_playwright() as playwright:
        # 在Chromium浏览器中创建一个新的浏览器上下文
        # browser = playwright.chromium.launch()
        browser = playwright.chromium.launch(
            #    proxy={"server": f"http://{ip}:{port}"}
            proxy={"server": f"http://127.0.0.1:7890"}
        )
        context = browser.new_context()

        # 创建一个新的页面并打开本地HTML文件
        page = context.new_page()
        page.goto(url)

        # 等待页面加载完成
        page.wait_for_load_state()

        # 获取页面标题
        title = page.title()
        print(f"title: {title} url: {url}")

        # 查找所有符合要求的元素
        # elements = page.query_selector_all(".fav-list-container li.fav-item a")
        # # 获取元素的文本数据
        # text_data = [element.text_content() for element in elements]

        # 关闭浏览器上下文
        context.close()
        browser.close()
        return title


async def get_real_url_async(url):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context()

        page = await context.new_page()
        await page.goto(url)
        await page.wait_for_load_state()

        title = await page.title()
        print(title, url)

        await context.close()
        await browser.close()
        return title


import asyncio


def async_test():
    # 假设urls是包含100个链接的列表
    urls = [...]

    async def fetch_all_urls():
        tasks = [get_real_url_async(url) for url in urls]
        return await asyncio.gather(*tasks)

    asyncio.run(fetch_all_urls())


def is_valid_url(url):
    try:
        response = requests.head(url)  # 发送HEAD请求以获取响应头而不是整个页面内容
        print(response.status_code, url)
        return response.status_code != 404
    except requests.RequestException:
        return False


invalid_titles = ["你似乎来到了没有知识存在的荒原 - 知乎"]


def print_links(links):
    for i, (title, url) in enumerate(links):
        print(f"index:{i} title:{title} url:{url}")


def save_links(links):
    for i, (title, url) in enumerate(links):
        # 先检测url是否有效
        title = get_real_url(url)
        if title in invalid_titles:
            print(f"invalid_titles index:{i} title:{title} url:{url}")
        else:
            print(f"index:{i} title:{title} url:{url}")


if __name__ == "__main__":
    # print(getNowDateTime())
    # print(getNowDate())
    # print(getNowTime())
    # print(getTimeStamp(getNowDateTime()))
    # print(getDateTimeStr(datetime.now(tz=tz_utc_8).timestamp()))
    # file_path = "/Users/yutianran/Documents/MyPKM/MyNote/EzWorkflowy/🗂️Category书签/Android技术探索 - 知乎.md"
    # md_content = read_file(file_path)
    # find_lines_without_regex(md_content)
    # links = find_md_links(md_content)[:2]
    # save_links(links)

    # print_links(links)
    # test_log()
    # async def fetch_all_urls():
    #     tasks = [get_real_url_async(url) for i, (title, url) in enumerate(links)]
    #     return await asyncio.gather(*tasks)

    # asyncio.run(fetch_all_urls())
    ips_content = read_file("assets/ips.json")
    ips = json.loads(ips_content).get("obj")
    print("ips代理数量: " + str(len(ips)))
