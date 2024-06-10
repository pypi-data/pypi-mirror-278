# #!/usr/bin/python3
# # coding=utf-8


# import sys
# import os
# import time
# # from colorlog import ColoredFormatter
# # import colorlog
# import logging
# # from fishyer_helper import datetime_util
# from os.path import abspath, dirname, join
# from logging import handlers

# # import traceback
# def get_caller_file_name():
#     caller_frame = sys._getframe(1)
#     caller_file_name = os.path.basename(caller_frame.f_code.co_filename)
#     return caller_file_name

# # 打印函数Frame MyLogUtil.py:167 f1()
# def format_frame_str(frame):
#     func_name = frame.f_code.co_name
#     file_path = frame.f_code.co_filename
#     file_name = os.path.basename(file_path)
#     file_lineno = frame.f_lineno
#     return f"{file_name}:{file_lineno} {func_name}()"


# # 打印被装饰的函数Frame MyLogUtil.py:167 f1()->f2()
# def format_anno_frame_str(frame):
#     func_name = frame.f_code.co_name
#     file_path = frame.f_code.co_filename
#     file_name = os.path.basename(file_path)
#     file_lineno = frame.f_lineno
#     return f"{file_name}:{file_lineno} {func_name}()"


# # 打印所有函数Frame depth=回溯深度，无则回溯到最底层
# def get_frames(depth=float("inf")):
#     # print(f"depth: {depth}")
#     trace = sys._getframe(0)
#     str = format_frame_str(trace)
#     print_depth = 0
#     while trace.f_back and print_depth <= depth:
#         str = format_frame_str(trace.f_back)
#         # logger.debug(f"{print_depth} {str}")
#         trace = trace.f_back
#         print_depth = print_depth + 1
#         # print(f"{print_depth} < {depth}")
#     return str


# # 获取对象
# def get_logger():
#     # 配置输出路径
#     project_dir = dirname(dirname(abspath(__file__)))
#     log_dir = join(project_dir, "log")
#     # 如果不存在log文件夹，则创建
#     if not os.path.exists(log_dir):
#         os.makedirs(log_dir)
#     date = datetime_util.get_now_date()
#     # 获取调用log工具类的文件名
#     caller_filename = os.path.basename(sys._getframe(1).f_code.co_filename)
#     # real_print(f"caller_filename: {caller_filename}")
#     caller_filename_without_ext = os.path.splitext(caller_filename)[0]
#     log_path = join(log_dir, f"{caller_filename_without_ext}_{date}.log")
#     # 配置输出格式 [常见日志参数](https://www.cnblogs.com/nancyzhu/p/8551506.html ) %(funcName)s %(filename)s:%(lineno)d
#     color_log_format = "%(log_color)s[%(levelname)1.1s] %(asctime)s %(message)s"
#     # file_log_format = "%(asctime)s | %(levelname)-8s | %(message)s"
#     file_log_format = "[%(levelname)1.1s] %(asctime)s %(message)s"
#     LOG_LEVEL = logging.DEBUG
#     # 配置日志级别
#     logging.root.setLevel(LOG_LEVEL)
#     # 设置控制台输出
#     stream_handler = logging.StreamHandler()
#     stream_handler.setLevel(LOG_LEVEL)
#     color_formatter = logging.Formatter(
#         "%(log_color)s[%(levelname)1.1s] %(asctime)s %(message)s %(reset)s %(blue)s",
#         datefmt="%Y-%m-%d %H:%M:%S",
#         reset=True,
#         log_colors={
#             "DEBUG": "cyan",
#             "INFO": "green",
#             "WARNING": "yellow",
#             "ERROR": "red",
#             "CRITICAL": "red,bg_white",
#         },
#         secondary_log_colors={},
#         style="%",
#     )
#     # stream_handler.setFormatter(ColoredFormatter(color_log_format,datefmt='%Y-%m-%d %H:%M:%S'))
#     stream_handler.setFormatter(color_formatter)
#     # 设置文件输出
#     # 往文件里写入#指定间隔时间自动生成文件的处理器
#     # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，
#     # when是间隔的时间单位，单位有以下几种：S-秒 M-分 H-小时 D-天 W-每星期 interval==0时代表星期一 midnight-每天凌晨
#     file_handler = handlers.TimedRotatingFileHandler(
#         filename=log_path, when="D", backupCount=5, encoding="utf-8"
#     )
#     file_handler.setFormatter(logging.Formatter(file_log_format))
#     # 最终创建的Logger对象
#     logger = logging.getLogger(log_path)
#     logger.setLevel(LOG_LEVEL)
#     logger.addHandler(stream_handler)
#     logger.addHandler(file_handler)
#     return logger


# # 给msg加上文件名和行号的装饰器
# def format_msg(msg, depth=0):
#     # 为-1时就不加前缀了
#     if depth == -1:
#         return msg
#     prefix = get_frames(depth)
#     msg = f"{prefix} | {msg}"
#     return msg


# # 封装一个可以接受多个参数的log方法
# def log(*args, depth=2):
#     msg = ""
#     for arg in args:
#         msg = msg + str(arg) + " "
#     logger.debug(format_msg(msg, depth))


# # 用装饰器，修改msg为format_msg
# def msg_wrapper(func):
#     def wrapper(*args, **kwargs):
#         msg = args[0]
#         format_msg_str = format_msg(msg, 2)
#         # print(f"msg: {msg}")
#         # print(f"format_msg: {format_msg}")
#         func(format_msg_str, **kwargs)

#     return wrapper


# # 封装几个简单的方法，以供外界调用
# # 调试信息
# # 主要有装饰器自动添加的参数打印
# def debug(msg, depth=2):
#     logger.debug(format_msg(msg, depth))


# # 日常开发信息-默认
# @msg_wrapper
# def info(msg):
#     logger.info(msg)


# # 重要警告信息
# @msg_wrapper
# def warning(msg):
#     logger.warning(msg)


# # 错误信息
# @msg_wrapper
# def error(msg):
#     logger.error(msg)


# @msg_wrapper
# def critical(msg):
#     logger.critical(msg)


# real_print = print
# print = log
# printf = log
# logger = get_logger()


# def test():
#     print(f"{__file__} {__name__}")
#     debug("This is debug.")
#     info("This is info.")
#     warning("This is warning.")
#     error("This is error.")
#     critical("This is critical.")
#     log("This is log.")
#     print("This is print.")


# if __name__ == "__main__":
#     print(f"START-TEST")
#     start_time = time.time()
#     test()
#     end_time = time.time()
#     print(f"END-TEST 耗时：{int((end_time - start_time)*1000)}ms")
# else:
#     print(f"__name__: {__name__}")
