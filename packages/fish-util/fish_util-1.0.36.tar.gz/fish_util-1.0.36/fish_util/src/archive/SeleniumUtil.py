import TimeUtil
from lxml import etree
import SeleniumCache,FileUtil,LogUtil
from urllib.parse import urlparse

from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
import time

print("start-fishyer")

def initSelenium():
    global browser
    options = ChromeOptions()
    options.add_argument("--headless")  # => 为Chrome配置无头模式
    # options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # options.add_experimental_option('useAutomationExtension', False)
    chromeDriverPath = "C:/Users/Administrator/Dropbox/MyTool/chromedriver.exe"
    browser =Chrome(options=options,executable_path=chromeDriverPath)
    # browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    #     "source": """
    #         Object.defineProperty(navigator, 'webdriver', {
    #         get: () => undefined
    #         })
    #     """
    #     })

def getWebpage(url):  # 获取网页
    browser.get(url)
    page_source = browser.page_source
    return page_source

def getHtmlWithCache(url):
    if url in cache:
        print("从本地读取："+url)
        out_path = cache[url]
        html = FileUtil.readFile(out_path)
        return html
    else:
        print("从网络读取："+url)
        html = getWebpage(url)
        out_path = f"C:/Users/Administrator/Dropbox/MyGithub/MyPython/build/page/page-{TimeUtil.getFoarmatNanoTimestamp()}.html"
        FileUtil.writeStr(html, out_path)
        cache[url] = out_path
        SeleniumCache.writeCache(cache)
        return html

def getRunoobTutorial(tutorial):  # 菜鸟教程-具体教程
    print("getRunoobTutorial", tutorial)
    parse = urlparse(tutorial)
    domain = parse.hostname
    scheme = parse.scheme
    path = parse.path
    html = getHtmlWithCache(tutorial)
    sel = etree.HTML(html)
    el = sel.xpath("//*[@id=\"leftcolumn\"]/a|//h2[@class=\"left\"]")
    # el = sel.xpath("//h2[@class=\"left\"]/span")
    md = ""
    name = "name"
    name_el = sel.xpath("//div[@class=\"tab\"]/span/text()")
    # https://www.runoob.com/html/html-tutorial.html
    if len(name_el):
        print("标准格式------------")
        name = name_el[0].strip().replace(" ", "-").replace("/", "-")
        print("name", name)
        md += (f"- 来源：[{name}]({tutorial})\n")
        for i in el:
            if i.tag == "h2":
                span = i.xpath("string(.)")
                print("- ", span, i.tag)
                md += (f"- {span}\n")
            elif i.tag == "a":
                t = i.xpath("@title")
                title = ""
                if len(t) == 0:
                    title = i.xpath("string(.)").strip().replace(" ", "-")
                else:
                    title = i.xpath("@title")[0].strip().replace(" ", "-")
                href = i.xpath("@href")[0]
                print("- ", title, f"{scheme}://{domain}{href}")
                md += (f"- [{title}]({scheme}://{domain}{href})\n")
            else:
                print(f"```````````````[{i.tag}]``````````````````")
        path = f"C:/Users/Administrator/Dropbox/MyObsidian/MyProgramTutorial/pages/{name}.md"
        writeStr(md, path)
    # https://www.runoob.com/w3cnote/zookeeper-tutorial.html list-link
    else:
        print("奇葩样式---------------------")
        name_el = sel.xpath("//div[contains(@class,\"list-link\")]/a")
        name = name_el[0].xpath("string(.)").strip().replace(" ", "-")
        print("name:", name)
        md += (f"- 来源：[{name}]({tutorial})\n")
        el = sel.xpath("//ul[@class=\"membership\"]/li")
        for i in el:
            title = i.xpath("string(.)").strip().replace(" ", "-")
            children = i.getchildren()
            if len(children):
                href = children[0].xpath("@href")[0]
                print("tilte:", title, href)
                md += (f"- [{title}]({href})\n")
            else:
                print("tilte:", title)
                md += (f"- {title}\n")
        path = f"C:/Users/Administrator/Dropbox/MyObsidian/MyProgramTutorial/pages/{name}.md"
        writeStr(md, path)

def startRunoob(urls):
    startUrl = "https://www.runoob.com/"
    html = getHtmlWithCache(startUrl)
    sel = etree.HTML(html)
    codelist_desktop = sel.xpath(
        "//div[contains(@class,\"codelist-desktop\")]")
    print(len(codelist_desktop))
    scheme = urlparse(startUrl).scheme
    md = ""
    for i in codelist_desktop:
        children = i.getchildren()
        if len(children):
            for e in children:
                if e.tag == "h2":
                    h2 = e.xpath("string(.)").strip()
                    md += f"## {h2}\n"
                if e.tag == "a":
                    h4 = e.getchildren()[0].xpath(
                        "string(.)").strip().replace("【", "").replace("】", "").replace("【", "").replace(" ", "")
                    herf = e.xpath("@href")[0]
                    link = f"{scheme}:{herf}"
                    md += (f"- [{h4}]({link})\n")
                    urls.append(link)
    name = "菜鸟教程-首页"
    path = f"C:/Users/Administrator/Dropbox/MyObsidian/MyProgramTutorial/site/{name}.md"
    writeStr(md, path)

# urls.append("https://www.runoob.com/java/java-tutorial.html")
# urls.append("https://www.runoob.com/nodejs/nodejs-tutorial.html")
# urls.append("https://www.runoob.com/python3/python3-tutorial.html")


cache = SeleniumCache.readCache()
urls = []
# startRunoob(urls)
# for i in urls:
#     getRunoobTutorial(i)

# # getRunoobTutorial("https://www.runoob.com/bootstrap/bootstrap-tutorial.html")
# print("done-fishyer")



def commonStrip(str):
    return str.replace('\n', '').replace('\r', '').replace(u'\xa0', '-').replace(" ", "").strip()

def addStageName(sel):
    el = sel.xpath(
        "//div[contains(@class,\"stage-name\")]/text()")
    for i in el:
        # 去掉换行符 &nbsp;表示的空格
        s=commonStrip(i)
        LogUtil.add(f"- {s}")

def addWeekName(sel):
    el = sel.xpath(
        "//div[contains(@class,\"week-name\")]/text()")
    for i in el:
        # 去掉换行符 &nbsp;表示的空格
        s=commonStrip(i)
        LogUtil.add(f"- {s}")

def addCourseContent(sel):
    el = sel.xpath(
        "//div[@class=\"content\"]/div[@class=\"text\"]/text()")
    # LogUtil.add(f"- {el[0]}")
    for i in el:
        s=commonStrip(i)
        if len(s)!=0:
            LogUtil.add(f"- {s} {len(s)}")\

def addStageNameWithSub(sel):
    el = sel.xpath(
        "//div[contains(@class,\"stage-section\")]")
    for e in el:
        # 获取e的所有子节点
        child=e.xpath("child::*")
        for c in child:
            clazz=c.xpath("@class")[0]
            if clazz=="top":
                stageNameEl=c.xpath("div[contains(@class,\"stage-name\")]/text()")[0]
                LogUtil.add(f"- {commonStrip(stageNameEl)}")
            if clazz=="week-name":
                weekNameEl=c.xpath("text()")[0]
                LogUtil.add(f"    - {commonStrip(weekNameEl)}")
            if clazz=="content":
                contentEl=c.xpath("div[@class=\"text\"]/text()")
                for j in contentEl:
                    content=commonStrip(j)
                    if len(content)!=0:
                        LogUtil.add(f"        - {content}")
    LogUtil.commit()


def getImoocCourse(url):
    html = getHtmlWithCache(url)
    sel = etree.HTML(html)
    addStageNameWithSub(sel)
    # 休眠100毫秒
    time.sleep(0.1)

def startImooc():
    url="https://class.imooc.com/"
    html=getHtmlWithCache(url)
    sel = etree.HTML(html)
    imoocEl=sel.xpath("//div[contains(@class,\"card\")]")
    for i in imoocEl:
        imoocName=i.xpath("@data-name")[0]
        imoocUrl=i.xpath("@data-url")[0]
        u=f"https:{imoocUrl}".replace("/sale", "")
        LogUtil.add(f"- 慕课网-{imoocName}")
        LogUtil.add(f"  - [{imoocName}]({u})")
        imoocUrls.append(u)
    LogUtil.commit()

imoocUrls=[]
initSelenium()
# startImooc()
imoocUrls.append("https://class.imooc.com/fearchitect")
imoocUrls.append("https://class.imooc.com/webfullstack2021")
imoocUrls.append("https://class.imooc.com/dataanalysis")
imoocUrls.append("https://class.imooc.com/computer")
for i in imoocUrls:
    getImoocCourse(i)