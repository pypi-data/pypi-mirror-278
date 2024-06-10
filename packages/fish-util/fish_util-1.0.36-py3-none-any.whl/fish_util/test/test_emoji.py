import os
import re
import emoji

print(emoji.emojize("Python is :thumbs_up:"))


def is_emoji(s):
    for char in s:
        if (
            "\U0001F600" <= char <= "\U0001F64F"  # Emoticons
            or "\U0001F300" <= char <= "\U0001F5FF"  # Symbols & Pictographs
            or "\U0001F680" <= char <= "\U0001F6FF"  # Transport & Map Symbols
            or "\U0001F700" <= char <= "\U0001F77F"  # Alchemical Symbols
            or "\U0001F780" <= char <= "\U0001F7FF"  # Geometric Shapes Extended
            or "\U0001F800" <= char <= "\U0001F8FF"  # Supplemental Arrows-C
            or "\U0001F900"
            <= char
            <= "\U0001F9FF"  # Supplemental Symbols and Pictographs
            or "\U0001FA00" <= char <= "\U0001FA6F"  # Chess Symbols
            or "\U0001FA70" <= char <= "\U0001FAFF"
        ):  # Symbols and Pictographs Extended-A
            return True
    return False


def remove_emoji(s):
    # 使用正则表达式进行替换
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub("", s)


def scan_files_with_emoji(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if is_emoji(file):
                file_without_emoji = remove_emoji(file)
                file_path = os.path.join(root, file)
                print(file_path, "=>", file_without_emoji)
                # 执行重命名操作
                # os.rename(file_path, os.path.join(root, file_without_emoji))
        for d in dirs:
            scan_files_with_emoji(os.path.join(root, d))


if __name__ == "__main__":
    # directory = input("请输入要扫描的文件夹路径: ")
    directory = "/Users/yutianran/Documents/MyNote/clipper-test"
    scan_files_with_emoji(directory)
