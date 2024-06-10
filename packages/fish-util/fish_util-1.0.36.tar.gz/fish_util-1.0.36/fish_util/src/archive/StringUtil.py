def real_strip(str):
    return str.strip().replace("\n", "").replace("\r", "")

def commonStrip(str):
    try:
        return str.replace('\n', '').replace('\r', '').replace(u'\xa0', '-').replace(" ", "").replace("，", "").replace("*", "").replace("\t", "").replace("(", "").replace("（", "").replace(")", "").replace("）", "").replace("/", "").strip()
    except :
        print("commonStrip-未知异常")
    return ""