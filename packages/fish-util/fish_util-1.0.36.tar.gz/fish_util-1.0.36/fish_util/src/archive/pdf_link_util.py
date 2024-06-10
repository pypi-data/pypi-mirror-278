import re

def format_md_link(file_path):
    # 提取文件名和扩展名
    match = re.search(r'/([^/]+)\.(\w+)$', file_path)
    if match:
        file_name = match.group(1)
        file_ext = match.group(2)
        # 格式化为Markdown格式的链接
        md_link = f"![{file_name}]({file_path})"
        return md_link
    else:
        return None

def test_file_path_with_spaces():
        file_path = "/Users/yutianran/Library/Application Support/DEVONthink 3/Inbox.dtBase2/Files.noindex/pdf/9/底层逻辑 看清这个世界的底牌（拥有看透世界的底牌，启动“开挂”的人生。“5分钟商学院”背后的思维方式）-刘润.pdf"
        expected_output = "![底层逻辑 看清这个世界的底牌（拥有看透世界的底牌，启动“开挂”的人生。“5分钟商学院”背后的思维方式）-刘润.pdf](/Users/yutianran/Library/Application Support/DEVONthink 3/Inbox.dtBase2/Files.noindex/pdf/9/底层逻辑 看清这个世界的底牌（拥有看透世界的底牌，启动“开挂”的人生。“5分钟商学院”背后的思维方式）-刘润.pdf)"
        print(format_md_link(file_path))
        # assert format_md_link(file_path)==expected_output

# test_file_path_with_spaces()