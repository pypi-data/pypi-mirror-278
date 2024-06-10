import os

dir = input('请输入一个目录：')
# dir=r"C:\Users\Administrator\Desktop\jupyter\testDir" #加r防止转义

def traverseFolder(dirPath):
    #获取目录列表
    listDir = os.listdir(dirPath)
    #遍历目录列表
    for path in listDir:
        fullPath=os.path.join(dirPath,path)
        # 是文件夹的话，就先打印文件夹的名称，再去遍历这个子文件夹
        if os.path.isdir(fullPath):
            print(fullPath)
            traverseFolder(fullPath)
        # 是文件的话，直接打印就好了
        else:
            print(fullPath)

traverseFolder(dir)
print(dir)