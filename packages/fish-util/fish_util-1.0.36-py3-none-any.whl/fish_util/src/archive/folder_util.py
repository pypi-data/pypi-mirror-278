import os
import re

# 确定你的目录路径
directory = './html'

# 使用os.listdir获取所有文件名
files = os.listdir(directory)

# 创建一个空列表来保存数字
inbox = []

def get_number(file):
    # 遍历所有文件
    for file in files:
        # 检查文件是否以'bili-'开头并且是'.txt'文件
        if file.startswith('bili-') and file.endswith('.txt'):
            # 使用正则表达式获取文件名中的数字
            number = re.search(r'\d+', file)
            if number:
                # 添加数字到列表
                inbox.append(str(number.group()))
    # 打印结果
    print(f"inbox: {len(inbox)}")
    path="html/bili/success.txt"
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(inbox))
        print(f"file:///Users/yutianran/MyGithub/MyVSCode/test-fastapi/{path}")

def merge_file():
    inbox=[]
    # 遍历所有文件
    for file in files:
        # 检查文件是否以'bili-'开头并且是'.txt'文件
        if file.startswith('bili-') and file.endswith('.txt'):
            with open(os.path.join(directory,file), 'r', encoding='utf-8') as f:
                content=f.read()
                inbox.append(content)
    path="html/bili/merge.txt"
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(inbox))
        print(f"file:///Users/yutianran/MyGithub/MyVSCode/test-fastapi/{path}")

        
merge_file()