import sys
from os.path import abspath, dirname, join
scriptRootDir = dirname(dirname(abspath(__file__)))
print("scriptRootDir",scriptRootDir)
sys.path.insert(0,scriptRootDir)

import util.FileUtil as FileUtil
import util.TimeUtil as TimeUtil

dirPath=join(scriptRootDir,"build") 

dest=join(dirPath,"log.md")

md=""

# 先收集
def add(src):
    global md
    print("log",src)
    md=md+src+"\n"

# 再输出
def commit(ext=".md"):
    global md
    print("commit")
    tf=TimeUtil.getFoarmatNanoTimestamp()
    dir = f"{dirPath}/{tf}{ext}"
    FileUtil.writeStr(md,dir)
    md=""

# 打印字符串到指定文件-覆盖
def log(src):
    print("log",src)
    tf=TimeUtil.getFoarmatTimestamp()
    dir = f"{dirPath}/{tf}.md"
    FileUtil.writeStr(src,dir)

# 打印字符串到指定文件-覆盖
def logw(src):
    print("log",src)
    tf=TimeUtil.getFoarmatTimestamp()
    content = f"{tf}:{src}\n"
    FileUtil.writeStr(content,dest)

# 打印字符串到指定文件-增量
def loga(src):
    print("log",src)
    tf=TimeUtil.getFoarmatTimestamp()
    content = f"{tf}:{src}\n"
    FileUtil.writeStrAppend(content,dest)

def main():
    log("12131213")

if __name__ == "__main__":
    main()