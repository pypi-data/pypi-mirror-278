import logging
import os
import time
from logging.handlers import RotatingFileHandler
import threading

tag = "logging"

# 创建日志文件夹
log_dir = "log"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 配置 logging 模块
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f'{log_dir}/{tag}_{time.strftime("%Y%m%d")}.log'),
        logging.StreamHandler(),
    ],
)

# 创建 RotatingFileHandler，将日志保存到 log 文件中，最多保存 5 个备份文件，每个备份文件最大为 1 MB
handler = RotatingFileHandler("app.log", maxBytes=1024 * 1024, backupCount=5)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
)
handler.setFormatter(formatter)


def print(msg):
    logging.info(msg)


def debug(msg):
    logging.debug(msg)


def info(msg):
    logging.info(msg)


def warn(msg):
    logging.warning(msg)


def error(msg):
    logging.error(msg)


logging.info(
    "-------------------------------[程序开始]-------------------------------------"
)

getcwd = os.getcwd()
print("getcwd: " + getcwd)
# /Users/yutianran/MyGithub/MyCode

abspath = os.path.abspath(__file__)
print("abspath: " + abspath)
# /Users/yutianran/MyGithub/MyCode/python/lib/log_util.py

module_name = __name__
print("module_name: " + module_name)

thread_name = threading.current_thread().name
print("thread_name: " + thread_name)
