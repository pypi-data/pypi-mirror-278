import os
import FileUtil,TimeUtil

# hulu导出数据/2022-04-01.md -> journals/2022_04_01.md，没办法，为了兼容Logseq的日志格式
def renameFileByDate(path):
    name =FileUtil.getFileName(path)
    srcDir = FileUtil.getFileDir(path)
    ext =FileUtil.getFileExt(path)
    if "-" in name:
        destName = TimeUtil.convertDataFormat(name)
        if destName=="":
            print("跳过重命名",f"{srcDir}/{name}{ext}")
            return
        if os.path.exists(f"{destDir}/{destName}{ext}"):
            FileUtil.mergeFile(f"{srcDir}/{name}{ext}", f"{destDir}/{destName}{ext}")
        else:
            print(f"{srcDir}/{name}{ext}", "->", f"{destDir}/{destName}{ext}")
            os.rename(f"{srcDir}/{name}{ext}", f"{destDir}/{destName}{ext}")

srcDir=r"D:\下载\2022-06-19下午10_32_12导出葫芦笔记数据"
destDir = "D:/Dropbox/MyObsidian/MyLogNote/journals"

FileUtil.traverseDirWithProcess(srcDir, renameFileByDate)
