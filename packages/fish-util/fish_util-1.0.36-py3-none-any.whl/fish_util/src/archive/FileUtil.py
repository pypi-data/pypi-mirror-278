import sys
from os.path import abspath, dirname
scriptRootDir = dirname(dirname(abspath(__file__)))
print("scriptRootDir",scriptRootDir)
sys.path.insert(0,scriptRootDir)

from fileinput import filename
import os
from datetime import datetime
import json

path=os.path.abspath(__file__)

def main():
    print("-------------------[main]-------------------")
    printPath(path)

# 打印文件路径
def printPath(path):  
    print(path)
    print(os.path.dirname(path), ".dir")
    print(os.path.basename(path), ".basename")
    print(os.path.splitext(path)[0], ".stem")
    print(os.path.splitext(path)[1], ".ext")
    print(os.path.splitext(os.path.basename(path))[0])

printPath(path)

# 返回带后缀名的文件名,eg:2022-06-15.md
def getFileExt(path):
    return os.path.basename(path)

# 返回文件的后缀名，可能为空，eg:.md
def getFileExt(path):
    return os.path.splitext(path)[1]

# 返回文件所在的文件夹，eg:C:/Users/Administrator/Dropbox/MyGithub/MyPython/2022-06-15下午2_10_05导出葫芦笔记数据
def getFileDir(path):
    return os.path.dirname(path)

# 返回无后缀名的文件名，eg:2022-06-15
def getFileName(path):
    return os.path.splitext(os.path.basename(path))[0]

# 在同一文件夹下的两个文件，重命名
def renameFileInDir(dir,src,dest):
    fileName=os.path.join(dir,src)
    newFileName=os.path.join(dir,dest)
    print(fileName,"->",newFileName)
    os.rename(fileName,newFileName)

# 增量写入
def writeStrAppend(val, path):
    file = open(path, "a", encoding='utf-8')
    file.write(val)
    file.flush()
    file.close()
    print(f"增量写入文本到文件成功：{path}")

# 合并文件
def mergeFile(src, dest):
    print("mergeFile",src,dest)
    s=readFile(src)
    tf=datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    content=f"\n\n## MergeFile-{tf}\n\n"+s
    writeStrAppend(content,dest)
    os.remove(src)

# 遍历文件夹
def traverseDir(dir):  
    files = os.listdir(dir)
    for file in files:
        if not os.path.isdir(file):
            f = open(f"{dir}/{file}")
            name = os.path.splitext(os.path.basename(file))[0]
            print(name)

# 遍历文件，一行行遍历，读取文本
def readFileWithLines(file):  
    str = ""
    iter_f = iter(file)
    for line in iter_f:
        str = str + line
    return str

# 读取文件
def readFile(path):  
    str = ""
    with open(path, 'r', encoding='utf-8') as f:
        str = f.read()
    print(f"读取文件成功：{path}")
    return str

# 读取json到map
def read_map(path):
    json_str = readFile(path)
    return json.loads(json_str)


# 遍历文件夹,对每个文件都做一种操作
def traverseDirWithProcess(dir, process):  
    files = os.listdir(dir)
    if len(files)==0:
        print("没有需要操作的文件",dir)
        return
    for file in files:
        if not os.path.isdir(file):
            # f = f"{dir}/{file}"
            f=os.path.join(dir,file)
            process(f)

# 写入map到文件,按json格式保存
def writeMap(val, path):
    file = open(path, "w", encoding='utf-8')
    json_str = json.dumps(
        val, indent=4, ensure_ascii=False, separators=(',', ':'))
    file.write(json_str)
    file.flush()
    file.close()
    print(f"写入map到文件成功：{path}")

# 写入文本到文件
def writeStr(val, path):  # 写入文本到文件
    if os.path.exists(path):
        os.remove(path)
    with open(path, 'w', encoding='utf-8') as file:
        file.write(val)
        print(f"写入文本到文件成功：",path)

# 增量写入文本到文件
def writeStrAppend(val, path):
    file = open(path, "a", encoding='utf-8')
    file.write(val)
    file.flush()
    file.close()
    print(f"增量写入文本到文件成功：{path}")

# 增量写入文本到文件-在头部添加
def writeStrAppendHead(val, path):
    src = ""
    if os.path.exists(path):
        src = read_file(path)
    file = open(path, "w")
    content = val+"\n"+src
    file.write(content)
    file.flush()
    file.close()
    print(f"增量写入文本到文件头部成功：{path}")

# 写入列表到文件
def writeList(val, path):
    file = open(path, "w")
    file.write('\n'.join(val))
    file.flush()
    file.close()
    print(f"写入列表到文件成功：{path}")


# 过滤掉Mac系统默认的.DS_Store文件
def isnotDsStore(val):
    if not re.match('^.*[.]DS_Store$', val):
        return True
    else:\
        return False

def traverseFolder(dirPath,process):
    #获取目录列表
    listDir = os.listdir(dirPath)
    #遍历目录列表
    for path in listDir:
        fullPath=os.path.join(dirPath,path)
        # 是文件夹的话，就先打印文件夹的名称，再去遍历这个子文件夹
        if os.path.isdir(fullPath):
            # print(fullPath)
            traverseFolder(fullPath,process)
        # 是文件的话，直接处理就好了
        else:
            process(fullPath)

def delete(path):
    end=path[-7:]
    # print(path)
    li=["(1).pdf","(2).pdf","(1).mp3","(2).mp3"]
    if end in li:
        # os.remove(path)
        print(path)

if __name__ == '__main__':
    main()



