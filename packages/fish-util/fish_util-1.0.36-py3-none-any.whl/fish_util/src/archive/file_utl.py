import os

# 检查文件路径是否存在，如果不存在则创建
def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

# 写入文件
def write_to_file(filename, content):
    try:
        with open(os.path.join(os.getcwd(), filename), 'a') as f:
            f.write(content)
        return 0
    except Exception as e:
        print(e)
        return 1

def test_write_to_file():
    result = write_to_file('test1.txt', "testContent")
    if result == 0:
        print('写入成功')
    else:
        print('写入失败')