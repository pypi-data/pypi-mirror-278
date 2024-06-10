import time


class StringBuilder:
    def __init__(self):
        self.strings = []

    def append(self, new_str):
        self.strings.append(new_str + "\n")

    def to_string(self):
        return "".join(self.strings)

    def clear(self):
        self.strings = []


def clean_file_name(title):
    # 将标题中的空格替换为无
    title = title.replace(" ", "")
    # 将文件名不能使用的字符有“\ / : * ? " < > | ”替换为中划线
    title = title.replace("\\", "")
    title = title.replace("/", "-")
    title = title.replace(":", "-")
    title = title.replace("*", "-")
    title = title.replace("?", "-")
    title = title.replace('"', "-")
    title = title.replace("<", "-")
    title = title.replace(">", "-")
    title = title.replace("|", "-")
    return title


def test():
    print(f"{__file__} {__name__}")
    # 使用示例
    builder = StringBuilder()
    builder.append("Hello")
    builder.append("World")
    print(builder.to_string())  # ==> "Hello\nWorld\n"
    builder.clear()


if __name__ == "__main__":
    print(f"START-TEST")
    start_time = time.time()
    test()
    end_time = time.time()
    print(f"END-TEST 耗时：{int((end_time - start_time)*1000)}ms")
else:
    print(f"__name__: {__name__}")
