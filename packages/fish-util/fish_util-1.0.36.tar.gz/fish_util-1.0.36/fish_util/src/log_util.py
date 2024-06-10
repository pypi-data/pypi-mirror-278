import time
import sys
import os
import inspect


def is_running_in_integrated_terminal():
    try:
        # 在集成终端中运行时，sys.stdout.isatty()返回True，区别于在输出面板中运行
        is_tty = sys.stdout.isatty()
        print("is_tty:", is_tty)
        return is_tty
    except:
        return False


# 获取调用者的栈帧,以便于定位日志输出位置
def get_caller_frame(parent_level=0):
    frame = inspect.currentframe()
    for _ in range(parent_level + 2):
        frame = frame.f_back
    return frame


# 日志控制器
class FishLogger:

    def __init__(
        self, path=None, tag=None, has_color=is_running_in_integrated_terminal()
    ):
        # 不设置path时，默认使用当前文件名作为日志文件名
        if path:
            self.path = path
        else:
            self.path = __file__
        # 不设置tag时，默认使用文件名作为tag
        if tag:
            self.tag = tag
        else:
            self.tag = os.path.basename(self.path)
        self.log_path = (
            f"{os.path.dirname(self.path)}/log/{os.path.basename(self.path)}.log"
        )
        if not os.path.exists(os.path.dirname(self.log_path)):
            os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        self.terminal = sys.stdout
        self.log_fd = open(self.log_path, "a+", encoding="utf-8")
        self.has_color = has_color
        self.write("")
        self.print("")
        divider_msg = "###################################################"
        self.warning(divider_msg)
        # self.debug(f"path: {self.path}")
        self.debug(f"log_path: {self.log_path}")
        # self.debug(f"tag: {self.tag}")
        # self.debug(f"has_color: {self.has_color}")

    def debug(self, msg):
        self.record("DEBUG", msg)

    def info(self, msg):
        self.record("INFO", msg)

    def warning(self, msg):
        self.record("WARN", msg)

    def error(self, msg):
        self.record("ERROR", msg)

    def msg_wrapper(self, level, msg, caller_level=2):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        level_padded = level.ljust(5)  # 使用 ljust 方法填充字符串，使得长度为 5
        caller_frame = get_caller_frame(caller_level)
        file_name = caller_frame.f_code.co_filename
        line_number = caller_frame.f_lineno
        func_name = caller_frame.f_code.co_name
        base_name = os.path.basename(file_name)
        new_msg = f"[{timestamp}] [{level_padded}] [{self.tag}] {base_name}:{line_number} {func_name}() - {msg}"
        return new_msg

    # 日志级别到颜色的映射字典
    level_colors = {"DEBUG": "blue", "INFO": "green", "WARN": "yellow", "ERROR": "red"}

    # 添加 ANSI 转义码来着色日志消息
    def colorize(self, msg, color):
        if not self.has_color:
            return msg
        colors = {
            "red": "\033[91m",
            "green": "\033[92m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "magenta": "\033[95m",
            "cyan": "\033[96m",
            "white": "\033[97m",
            "reset": "\033[0m",
        }
        return f"{colors[color]}{msg}{colors['reset']}"

    def print(self, msg):
        sys_print(msg)
        # if self.terminal is not None:
        #     self.terminal.write(msg + "\n")
        #     self.terminal.flush()

    def write(self, msg):
        self.log_fd.write(msg + "\n")
        self.log_fd.flush()

    def record(self, level, msg, caller_level=2):
        msg = self.msg_wrapper(level, msg, caller_level)
        color = self.level_colors.get(level, "white")
        self.print(self.colorize(msg, color))
        self.write(msg)


sys_print = print
logger = FishLogger()
print = logger.debug


def test():
    print(__file__)


if __name__ == "__main__":
    test()
