import os
import re,EzUtil

# [name](link) -> <DT><A HREF="link">name</A>
def link_to_chrome_dt(mdlink):
    p = re.compile("\[(.+)\]\((http[s]?://.*)\)")
    chromelink=re.sub(p,lambda m:f"<DT><A HREF=\"{m.group(2)}\">{m.group(1)}</A>",mdlink)
    return chromelink

# [name](link) list -> chrome 书签
def linklist_to_chrome(linklist):
    list_item_str=""
    for item in linklist:
        chrome_link=link_to_chrome_dt(item)
        list_item_str=list_item_str+f"    {chrome_link}\n"
        # path = os.path.join(dir_path, item)
        # # 如果是md文件
        # if os.path.isfile(path) and path.endswith(".md"):
        #     md=read_file(path)
        #     find_list = pattern.findall(md)
        #     for find_item in find_list:
        #         chrome_link=mdlink_to_chromelink(find_item)
        #         list_item_str=list_item_str+f"    {chrome_link}\n"
    chrome_template="""<!DOCTYPE NETSCAPE-Bookmark-file-1>
    <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
    <TITLE>Bookmarks</TITLE>
    <H1>Bookmarks</H1>
    <DL><p>
        <DT><H3 ADD_DATE="1634759143" LAST_MODIFIED="1634759173" PERSONAL_TOOLBAR_FOLDER="true">书签栏</H3>
        <DL><p>
    {LIST_ITEM}
        </DL><p>
    </DL><p>
    """
    chrome_str=chrome_template.replace("{LIST_ITEM}",list_item_str)
    return chrome_str

# if __name__ == "__main__":
#     print("test print")
#     # 读取本地文件夹
#     dir_path="/Users/yutianran/Documents/MyObsidian/1-Pulish"
#     list=os.listdir(dir_path)
#     # 写入html文件
#     out_path="/Users/yutianran/Documents/MyObsidian/Cache/md_all.html"
#     ezutil.write_str(out_path,chrome_str)
