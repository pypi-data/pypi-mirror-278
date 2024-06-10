from lxml import html, etree
import fishyer_helper.file_util as file_util
import os
import re

def main():
    # 解析HTML文件
    path="html/bili-nav.html"
    with open(path, "r", encoding="utf-8") as f:
        str = f.read()
    print(f"读取文件成功：{path}")
    # html=file_util.read_file('html/bili-nav.html')
    # tree = etree.parse(str)
    tree = etree.HTML(str)

    # # 查找所有符合要求的元素
    # elements = tree.cssselect(".fav-list-container li.fav-item a")
    # elements = tree.cssselect("ul.fav-video-list li.small-item a.title")
    elements = tree.cssselect("ul.fav-list li.fav-item a.text")

    # # 获取元素的文本数据
    text_data = [ ]
    for element in elements:
        title=element.text
        # /481831994/favlist?fid=1744909&ftype=collect&ctype=21
        link=element.get("href")
        # string = "/481831994/favlist?fid=1744909&ftype=collect&ctype=21"
        match = re.search('fid=([0-9]+)', link)
        if title=="已失效视频":
            continue
        if title=="该合集已失效":
            continue
        if match:
            fid = match.group(1)
            print(f'fid: {fid}')
            text_data.append(fid)
    print(f"获取文本数据成功：{len(text_data)}")

    # # 将文本数据保存到文件
    path="html/bili/todo.txt"
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(text_data))
        print(f"file:///Users/yutianran/MyGithub/MyVSCode/test-fastapi/{path}")

from lxml import etree
html_doc='<html><body><div id="info"><div class="name">hello</div><div class="tips" title="tips">hello world</div></div></body></html>'
doc=etree.HTML(html_doc)
print(doc.cssselect('#info .name')[0].text)
print(doc.cssselect('.tips')[0].attrib)

# if __name__ == "__main__":
    # main()

