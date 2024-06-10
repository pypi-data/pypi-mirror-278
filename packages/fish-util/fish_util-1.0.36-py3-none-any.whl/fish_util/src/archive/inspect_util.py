import inspect

# 比__file__更好的方法
def current_file():
    frame = inspect.currentframe()
    file_name = frame.f_code.co_filename
    return file_name

print(current_file())
