import sys
import os

# 打印函数Frame MyLogUtil.py:167 f1()
def format_frame_str(frame):
    func_name = frame.f_code.co_name
    file_path = frame.f_code.co_filename
    file_name = os.path.basename(file_path)
    file_lineno = frame.f_lineno
    return f"{file_name}:{file_lineno} {func_name}()"

# 打印所有函数Frame depth=回溯深度，无则回溯到最底层
def get_frames(depth=float("inf")):
    # print(f"depth: {depth}")
    trace = sys._getframe(0)
    str = format_frame_str(trace)
    print_depth = 0
    while trace.f_back and print_depth <= depth:
        str = format_frame_str(trace.f_back)
        # logger.debug(f"{print_depth} {str}")
        trace = trace.f_back
        print_depth = print_depth + 1
        # print(f"{print_depth} < {depth}")
    return str

# 给msg加上文件名和行号的装饰器
def format_msg(msg, depth=0):
    # 为-1时就不加前缀了
    if depth == -1:
        return msg
    prefix = get_frames(depth)
    msg = f"{prefix} | {msg}"
    return msg

# 用装饰器，修改msg为format_msg
def msg_wrapper(func):
    def wrapper(*args, **kwargs):
        # print(f"args: {args}, kwargs: {kwargs}")
        msg = concat_args(*args[1:])
        # print(f"msg: {msg}")
        depth=get_tuple_value(kwargs, "depth", 2)
        # print(f"depth: {depth}")
        fmsg = format_msg(msg, depth)
        # print(f"fmsg: {fmsg}")
        return func(fmsg, **kwargs)
    return wrapper

# 安全的获取元组的值
def get_tuple_value(tuple_obj, key,default_vaule):
    if key in tuple_obj:
        return tuple_obj[key]
    else:
        return default_vaule

# 将多个*args合并为1个msg
def concat_args(*args):
    msg = ""
    for arg in args:
        msg = msg + " " + str(arg)
    return msg

def decorator(func):
    def wrapper(*args, **kwargs):
        print(f"args: {args}, kwargs: {kwargs}")
        return func(*args, **kwargs)
    return wrapper

@decorator
def func(a, b, c, name="Tom", age=20):
    print(f"a: {a}, b: {b}, c: {c}, name: {name}, age: {age}")


def main():
    print(f"start main function ...")
    func(1, 2, 3, name="Jerry", age=30)

if __name__ == "__main__":
    main()