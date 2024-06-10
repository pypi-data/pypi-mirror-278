import os
import json
from datetime import datetime
import shutil
import re
from fish_util.src.loguru_util import print, debug, info, warning, error


# 打印文件路径
def print_path(path):
    print(path)
    print(os.path.dirname(path), ".dir")
    print(os.path.basename(path), ".basename")
    print(os.path.splitext(path)[0], ".stem")
    print(os.path.splitext(path)[1], ".ext")
    print(os.path.splitext(os.path.basename(path))[0])


# 返回带后缀名的文件名,eg:2022-06-15.md
def get_file_ext(path):
    return os.path.basename(path)


# 返回文件的后缀名，可能为空，eg:.md
def get_ext(path):
    return os.path.splitext(path)[1]


# 返回文件所在的文件夹，eg:C:/Users/Administrator/Dropbox/MyGithub/MyPython/2022-06-15下午2_10_05导出葫芦笔记数据
def get_file_dir(path):
    return os.path.dirname(path)


# 返回无后缀名的文件名，eg:2022-06-15
def get_file_name(path):
    return os.path.splitext(os.path.basename(path))[0]


# 在同一文件夹下的两个文件，重命名
def rename_file_in_dir(dir, src, dest):
    file_name = os.path.join(dir, src)
    new_file_name = os.path.join(dir, dest)
    print(file_name, "->", new_file_name)
    os.rename(file_name, new_file_name)


# 增量写入
def write_str_append(val, path):
    with open(path, "a", encoding="utf-8") as file:
        file.write(val)
        print(f"增量写入文本到文件成功：{path}")


# 合并文件
def merge_file(src, dest):
    print("mergeFile", src, dest)
    s = read_file(src)
    tf = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    content = f"\n\n## MergeFile-{tf}\n\n" + s
    write_str_append(content, dest)
    os.remove(src)


# 遍历文件夹
def traverse_dir(dir):
    files = os.listdir(dir)
    for file in files:
        if not os.path.isdir(file):
            f = open(f"{dir}/{file}")
            name = os.path.splitext(os.path.basename(file))[0]
            print(name)


# 遍历文件，一行行遍历，读取文本
def read_file_with_lines(file):
    strs = []
    iter_f = iter(file)
    for line in iter_f:
        strs.append(line)
    return strs


# 读取文件
def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        str = f.read()
    # print(f"读取文件成功：{path}")
    return str


# 读取json到map
def read_map(path):
    json_str = read_file(path)
    return json.loads(json_str)


# 遍历文件夹,对每个文件都做一种操作
def traverse_dir_with_process(dir, process):
    files = os.listdir(dir)
    if len(files) == 0:
        print("没有需要操作的文件", dir)
        return
    for file in files:
        if not os.path.isdir(file):
            f = os.path.join(dir, file)
            process(f)


# 写入map到文件,按json格式保存
def write_map(val, path):
    with open(path, "w", encoding="utf-8") as file:
        json_str = json.dumps(val, indent=4, ensure_ascii=False, separators=(",", ":"))
        file.write(json_str)
        print(f"写入map到文件成功：{path}")


# 写入文本到文件
def write_str(val, path):  # 写入文本到文件
    if os.path.exists(path):
        os.remove(path)
    with open(path, "w", encoding="utf-8") as file:
        file.write(val)
        print(f"写入文本到文件成功：{path}")


# 增量写入文本到文件
def write_str_append(val, path):
    with open(path, "a", encoding="utf-8") as file:
        file.write(val)
        print(f"增量写入文本到文件成功：{path}")


# 增量写入文本到文件-在头部添加
def write_str_append_head(val, path):
    src = ""
    if os.path.exists(path):
        src = read_file(path)
    with open(path, "w") as file:
        content = val + "\n" + src
        file.write(content)
        print(f"增量写入文本到文件头部成功：{path}")


# 写入列表到文件
def write_list(val, path):
    with open(path, "w") as file:
        file.write("\n".join(val))
        print(f"写入列表到文件成功：{path}")


# 过滤掉Mac系统默认的.DS_Store文件
def is_not_ds_store(val):
    if not re.match("^.*[.]DS_Store$", val):
        return True
    else:
        return False


def traverse_folder(dir_path, process):
    # 获取目录列表
    list_dir = os.listdir(dir_path)
    # 遍历目录列表
    for path in list_dir:
        full_path = os.path.join(dir_path, path)
        # 是文件夹的话，就先打印文件夹的名称，再去遍历这个子文件夹
        if os.path.isdir(full_path):
            traverse_folder(full_path, process)
        # 是文件的话，直接处理就好了
        else:
            process(full_path)


def check_path(path):
    if not os.path.exists(path):
        print(f"路径不存在：{path}")
        return False
    return True


def sure_dir(path):
    if path == "":
        print(f"文件夹路径为空：{path}")
        return
    if not os.path.exists(path) and path != "":
        os.makedirs(path)
        print(f"创建文件夹成功：{path}")
    else:
        # print(f"文件夹已存在：{path}")
        pass


def sure_file(path):
    if path == "":
        print(f"文件路径为空：{path}")
        return
    if not os.path.exists(path):
        with open(path, "w") as file:
            # file.write("")
            # print(f"创建空白文件成功： {path}")
            pass
    else:
        print(f"文件已存在： {path}")


def sure_path(path):
    if path == "":
        print(f"路径为空：{path}")
        return
    if os.path.isdir(path):
        sure_dir(path)
    else:
        file_dir = get_file_dir(path)
        sure_dir(file_dir)
        sure_file(path)


# 如果path是文件夹，就删除文件夹下的所有文件，如果path是文件，就删除文件
def delete(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.isfile(path):
        os.remove(path)
    else:
        print(f"Error: {path} 不是文件夹，也不是文件.")


def delete_match(path):
    end = path[-7:]
    li = ["(1).pdf", "(2).pdf", "(1).mp3", "(2).mp3"]
    if end in li:
        print(path)


def test():
    path = __file__
    print_path(path)


if __name__ == "__main__":
    test()
