import sys

def is_running_in_integrated_terminal():
    try:
        # 在集成终端中运行时，sys.stdout.isatty()返回True，区别于在输出面板中运行
        is_tty=sys.stdout.isatty()
        print("is_tty:", is_tty)
        return is_tty
    except:
        return False

if is_running_in_integrated_terminal():
    print("Python script is running in Integrated Terminal.")
else:
    print("Python script is not running in Integrated Terminal.")
