import base64
from doctest import FAIL_FAST
import os
import sys
import hashlib
import frontmatter
from io import StringIO
import webbrowser
import markdown2
from bs4 import BeautifulSoup
import yaml
import re
import datetime
import shutil

testMode = 0
stringIO = StringIO()
defaultYuqueDir = "D:\Dropbox\MyObsidian\MyLogseq\MyYuque"
testMdPath = r"D:\Dropbox\MyObsidian\MyLogseq\MyYuque\3-杂思之趣\Chrome-使用uBlacklist插件，清除内容农场，优化搜索结果.md"

#TODO: 这是待实现的功能点
#FIXME: 这是待修复的BUG
#XXX: 这是待重构 broadcast
#TAG: 这是标签记号，方便以后定位
#DONE: 这是需求点，可在注释或commit附上TAPD需求文档
#BUG: 这是已解决的BUG，可附上StackOverFlow的解决方案
def main():
    # python d:/Dropbox/MyObsidian/MyYuque/test/yuque_util.py d:/Dropbox/MyObsidian/MyYuque/test
    print("-------------------[main]-------------------")
    # currentDir=os.getcwd()
    # print("currentDir:", currentDir)
    postDirPath = getUploadDir()
    summaryPath = os.path.join(postDirPath, "summary.md")
    # 迭代获取文件名，最后写入目录文件中
    traverseDirWithProcess(postDirPath, myProcess, dirFilter=myDirFilter)
    writeStr(stringIO.getvalue(), summaryPath)
    # 非生产环境时，直接放弃后续的上传操作
    # processWaque(postDirPath)


def test():
    print("-------------------[test]-------------------")
    # processRegex(testMdPath)
    # test_current_path()


# 最后还是得用正则来处理啊
def processRegex(mdPath):
    print("-------------------[processRegex]-------------------")
    # lines=readFileLines(mdPath)
    with open(mdPath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    # 每一篇文章中只允许出现2次，从第3次出现，到最后一次出现，都需要删除
    occurrenceTimes = 0
    pattern = r"^---"
    isFirstFrontMatter = True
    start = -1
    end = -1
    for i in range(min(100000000, len(lines))):
        line = lines[i]
        # dest=re.sub(pattern,lambda m:f"[Matched] {m.group()}",line)
        # print(dest)
        matchObj = re.match(pattern, line)
        if matchObj:
            occurrenceTimes += 1
            if occurrenceTimes % 2 == 1:
                # lines=removeLines(lines,i,i+1)
                if not isFirstFrontMatter:
                    start = i + 1
                print(
                    f"------>>>>>>:  {start} {isFirstFrontMatter}",
                    matchObj.group(),
                    type(matchObj.group()),
                )
            else:
                # lines=removeLines(lines,i,i+1)
                if not isFirstFrontMatter:
                    end = i + 1
                isFirstFrontMatter = False
                print(
                    f"<<<<<<------:  {end} {isFirstFrontMatter}",
                    matchObj.group(),
                    type(matchObj.group()),
                )
            if start != -1 and end != -1:
                # mockLines=list(range(1,25))
                mockLines = lines.copy()
                subMockLines = removeLines(mockLines, start, end)
                print(f"mockLines: {len(mockLines)}")
                print(f"subMockLines: {len(subMockLines)}")
                bakFile = genBakFile(mdPath)
                with open(bakFile, "w", encoding="utf-8") as fw:
                    fw.writelines(subMockLines)


# 备份文件
def genBakFile(path):
    print(f"-------------------[genBakFile: {path}]-------------------")
    bakPath = getBackupFileName(path)
    print("getBackupFileName:", bakPath)
    # shutil.copyfile(path,bakPath)
    # print(f"shutil.copyfile({path},{bakPath})")
    return bakPath


# 生成一个备份文件名称
def getBackupFileName(path):
    nowTimePath = datetime.datetime.now().strftime("%Y-%m-%d____%H-%M-%S")
    name = getPathName(path)
    ext = getPathExt(path)
    dir = os.path.dirname(path)
    backupPath = os.path.join(dir, f"{name}-bak-{nowTimePath}{ext}")
    return backupPath


# 删除指定行 [start,end) 从1开始计算行数
def removeLines(lines, start, end):
    print(f"-------------------[removeLines: {start} -> {end} ]-------------------")
    sub = lines[: start - 1] + lines[end:]
    return sub


# # 按行处理
# def readFileLines(mdPath):
#     f  =  open(mdPath, 'r', encoding='utf-8')
#     result=[]
#     while  True :
#         lines=f.readlines( 10000 )
#         result.extend(lines)
#         if not lines:
#             break
#         for  line  in  lines:
#             # print (line)
#             pass
#     f.close()
#     return result

# py脚本不传参数的话，就以默认的defaultYuqueDir为参数
def getUploadDir():
    args = sys.argv
    print("args:", args)
    # uploadDir=args[1] if len(args)>1 else os.getcwd()
    uploadDir = args[1] if len(args) > 1 else defaultYuqueDir
    print("uploadDir:", uploadDir)
    return uploadDir


# 处理瓦雀相关的操作
def processWaque(postDirPath):
    cmd = f"cd {postDirPath} && waque upload"
    print("cmd:", cmd)
    cmdCode = os.system(cmd)
    if cmdCode == 0:
        repo = getYamlDict()["repo"]
        targetUrl = f"https://www.yuque.com/{repo}"
        webbrowser.open(targetUrl, new=0, autoraise=True)
        print("open browser done:", targetUrl)


def myDirFilter(path):
    name = getPathName(path)
    # 不处理.git .husky node_modules 等文件夹 以及其它以.开头的文件夹
    if name in [".git", ".husky", "node_modules"] or name.startswith("."):
        print(f"myDirFilter-false: {path}")
        return False
    return True


# MD5加密出来的是一串16进制数,正好符合yuque的url的格式要求，之前试过Base64，但是不行，这里就用MD5当做默认的url
def myProcess(wrapper):
    global stringIO
    path = wrapper.path
    name = getPathName(path)
    prefix = "    " * wrapper.level
    if os.path.isdir(path) and myDirFilter(path):
        formatStr = f"{prefix}- [{name}]()"
        stringIO.write(formatStr + "\n")
        print(f"add dir to summary: {path}")
    else:
        ext = getPathExt(path)
        # 不处理非md文件
        if ext != ".md":
            return
        # 不处理summary.md文件
        if name == "summary":
            print(f"删除已存在的summary: {path}")
            os.remove(path)
            return
        # 1-处理md文件的Frontmatter属性
        myMetadata = processFrontmatter(path)
        url = myMetadata["url"]
        # public==0，表示私密，不需要添加到目录中，以免隐私泄露，虽然点击目录中的标题以后是404，但私有笔记的标题也是一种隐私，没必要被别人看到
        # publiuc==1(默认值),表示公开，需要添加到目录中
        # if 'public' not in myMetadata or myMetadata['public'] is None or myMetadata['public']==1:
        if myMetadata.get("public", 1) == 1:
            formatStr = f"{prefix}- [{name}]({url})"
            stringIO.write(formatStr + "\n")
        # 2-处理md文件的markdown内容
        processMarkdown(path)


# 读取yaml文件，返回字典
def getYamlDict():
    currentDirPath = os.getcwd()
    yamlPath = os.path.join(currentDirPath, "yuque.yml")
    with open(yamlPath, "r", encoding="utf-8") as f:
        yamlConfig = f.read()
        yamlDict = yaml.load(yamlConfig, Loader=yaml.FullLoader)
        print("yamlDict:", yamlDict)
        return yamlDict
    raise Exception("read yaml fail")


# 读取markdown文件，并获取到h1属性
def processMarkdown(mdPath):
    # 先将markdown转html，再用beautifulsoup解析
    md = markdown2.Markdown()
    mdStr = readFile(mdPath)
    mdHtml = md.convert(mdStr)
    soup = BeautifulSoup(mdHtml, features="html.parser")
    h1Node = soup.select("h1")
    modify = False
    # 0个或大于1个的h1,都不是正常情况，要删掉所有h1，然后下面再生成一个h1
    name = getPathName(mdPath)
    if len(h1Node) != 1:
        for i in range(len(h1Node)):
            h1 = h1Node[i].getText().strip()
            mdStr = mdStr.replace(f"# {h1}\n", f"")
        print(f"compare title fail: name={name} h1.len={len(h1Node)} mdPath={mdPath}")
        modify = True
    if modify:
        # 直接在首行添加h1
        mdStr = f"# {name}\n\n" + mdStr
        writeStr(mdStr, mdPath)


# 读取fontmatter中的内容
def processFrontmatter(mdPath):
    isWrite = False
    name = getPathName(mdPath)
    # 先尝试读取原有的frontmatter属性
    with open(mdPath, "r", encoding="utf-8") as f:
        mdFrontmatter = frontmatter.load(f)
        if 1 == 1 or mdFrontmatter.get("url") is None:
            # 没有url,就自己根据name生成name_md5来做默认的url；已有url,就直接使用已有的url
            name_md5 = hashlib.md5(name.encode(encoding="utf-8")).hexdigest()
            mdFrontmatter["url"] = name_md5
            isWrite = True
    # 再将frontmatter属性写入md文件
    if isWrite:
        with open(mdPath, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(mdFrontmatter))
            print(f"write frontmatter done: {mdPath} {mdFrontmatter.metadata}")
    return mdFrontmatter.metadata


# 读取文件
def readFile(path):
    str = ""
    with open(path, "r", encoding="utf-8") as f:
        str = f.read()
    print(f"读取文件成功：{path}")
    return str


# 写入字符串到文件
def writeStr(str, path):
    if os.path.exists(path):
        os.remove(path)
    with open(path, "w", encoding="utf-8") as file:
        file.write(str)
        print(f"写入文本到文件成功：{path}")


class FileWrapper:
    def __init__(self, path, level=0):
        self.path = path
        self.level = level


# 获取文件的真实名称，不包括扩展名 dir\name.txt -> name
def getPathName(path):
    return os.path.splitext(os.path.basename(path))[0]


# 获取文件的后缀， dir\name.txt -> .txt
def getPathExt(path):
    return os.path.splitext(path)[1]


# 对字符串进行base64编码 abc -> YWJj
def encodeBase64(input):
    encodestr = base64.b64encode(input.encode("utf-8"))
    res = str(encodestr, "utf-8")
    return res


# 遍历文件夹,对每个文件都做一种操作
def traverseDirWithProcess(dir, process, level=0, dirFilter=None):
    files = os.listdir(dir)
    # 没有需要操作的文件时，直接返回
    if len(files) == 0:
        return
    for file in files:
        fullPath = os.path.join(dir, file)
        # 是文件夹的话，就循环遍历这个子文件夹
        filterResult = dirFilter is None or dirFilter(fullPath)
        if os.path.isdir(fullPath) and filterResult:
            process(FileWrapper(fullPath, level))
            traverseDirWithProcess(fullPath, process, level + 1, dirFilter)
        # 是文件的话，就直接处理
        else:
            process(FileWrapper(fullPath, level))


# 测试当前文件路径
def test_current_path():
    print("sys.path[0] = ", sys.path[0])
    print("sys.argv[0] = ", sys.argv[0])
    print("__file__ = ", __file__)
    print("os.path.abspath(__file__) = ", os.path.abspath(__file__))
    print("os.path.realpath(__file__) = ", os.path.realpath(__file__))
    print(
        "os.path.dirname(os.path.realpath(__file__)) = ",
        os.path.dirname(os.path.realpath(__file__)),
    )
    print(
        "os.path.split(os.path.realpath(__file__)) = ",
        os.path.split(os.path.realpath(__file__)),
    )
    print(
        "os.path.split(os.path.realpath(__file__))[0] = ",
        os.path.split(os.path.realpath(__file__))[0],
    )
    print("os.getcwd() = ", os.getcwd())
    print(
        "os.getUpload() = ",
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "upload"
        ),
    )


if __name__ == "__main__":
    if testMode:
        test()
    else:
        main()
