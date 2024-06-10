"""
初始化日志类
:param log_path: 日志文件存放路径
Loguru默认支持以下颜色：
    <black>
    <red>
    <green>
    <yellow>
    <blue>
    <magenta> 洋红
    <cyan> 蓝绿
    <white>
    你可以在这些颜色名称之后添加一个!来表示亮色。例如，<red!>将显示亮红色。
"""

from loguru import logger
import os
import sys
import time
import inspect

import fish_util.src.decorator_util2 as decorator_util

catcher = logger.catch


def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


def my_filter(record):
    return "my_filter" in record["extra"]


class LoguruLogger:
    def __init__(self, log_path="log/app"):
        # self.log_path = log_path
        check_path(log_path)
        # 移除默认的logger，添加自定义的logger
        logger.remove()
        # 将所有级别日志输出到控制台
        logger.add(
            sys.stderr,
            filter=my_filter,
            # format="<level>[{level}] {time:YYYY-MM-DD HH:mm:ss.SSS} {file}:{line} {function}() | {message}</level>",
            format="<level>[{level}] {time:YYYY-MM-DD HH:mm:ss.SSS} | {process.name}:{thread.name} | {message}</level>",
            colorize=True,
            level="DEBUG",
        )
        # 按级别将日志输出到不同的文件
        log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        logger.level("DEBUG", color="<blue>")
        logger.level("INFO", color="<green>")
        logger.level("WARNING", color="<yellow>")
        logger.level("ERROR", color="<red>")
        logger.level("CRITICAL", color="<magenta>")
        for level in log_levels:
            level_path = os.path.join(log_path, level.lower())
            check_path(level_path)
            logger.add(
                f"{level_path}/{level.lower()}-{{time:YYYY-MM-DD}}.log",
                rotation="00:00",
                # filter=my_filter,
                format="<level>[{level}] {time:YYYY-MM-DD HH:mm:ss.SSS} {file}:{line} {function}() | {message}</level>",
                colorize=False,
                level=level,
            )

    def get_logger(self):
        return logger

    # 封装几个简单的方法，以供外界调用
    # 调试信息
    # 主要有装饰器自动添加的参数打印
    def debug(self, *args, depth=2):
        msg = decorator_util.concat_args(*args)
        fmsg = decorator_util.format_msg(msg, depth)
        logger.debug(fmsg)

    # 日常开发信息-默认
    # @msg_wrapper
    @decorator_util.msg_wrapper
    def info(*msg):
        logger.info(msg[0])

    # 重要警告信息
    @decorator_util.msg_wrapper
    def warning(*msg):
        logger.warning(msg[0])

    # 错误信息
    @decorator_util.msg_wrapper
    def error(*msg):
        logger.error(msg[0])

    @decorator_util.msg_wrapper
    def critical(*msg):
        logger.critical(msg[0])

    # 封装一个可以接受多个参数的log方法
    def log(self, *args, depth=2):
        # 去掉0是因为0是self对象
        msg = decorator_util.concat_args(*args)
        fmsg = decorator_util.format_msg(msg, depth)
        logger.debug(fmsg)

    # 打印对象的属性和方法
    def cat_method(self, var):
        logger.debug(f"dir: {dir(var)}")

    # 打印变量的名称和值
    def cat(self, *args):
        callers_local_vars = inspect.currentframe().f_back.f_locals.items()
        for var in args:
            names = [k for k, v in callers_local_vars if v is var]
            for name in names:
                self.debug(f"{type(var)} {name}: {var}", depth=3)

    def raise_error(self, msg="结束程序"):
        raise Exception(msg)


def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


def my_filter(record):
    record["level"].name = record["level"].name[0]
    # record["level"].name = record["level"].name
    return True


def my_function(x):
    # An error? It's caught anyway!
    return 1 / x


def skip(*args, **kwargs):
    pass


def timing_and_display_args(func):
    logger = default_logger

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.info(
            f"Function {func.__name__} called with args {args} and kwargs {kwargs}"
        )
        logger.info(f"Function {func.__name__} returned {result}")
        logger.info(f"Function {func.__name__} took {end - start} seconds to complete")
        return result

    return wrapper


default_logger = LoguruLogger()

debug = default_logger.debug
info = default_logger.info
warning = default_logger.warning
error = default_logger.error
critical = default_logger.critical
print = default_logger.debug
cat = default_logger.cat


@catcher
def main():
    print(f"[run main: {__file__}]")
    logger = LoguruLogger()
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    logger.log("This is a log message")
    name = "test-cat"
    logger.cat(name)
    # my_function(0)


if __name__ == "__main__":
    main()
