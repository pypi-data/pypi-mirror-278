from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
import asyncio

from fake_useragent import UserAgent

ua = UserAgent()

# 生成Chrome浏览器的User-Agent
chrome_user_agent = ua.chrome
print(chrome_user_agent)


def sync_search(keyword):
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # 设置user-agent
        context = browser.new_context(user_agent=chrome_user_agent)
        page = context.new_page()

        page.goto("https://www.google.com")
        page.fill("[aria-label='Search'] [name='q']", keyword)
        page.press("[aria-label='Search'] [name='q']", "Enter")
        page.wait_for_selector("#search")

        search_results = page.query_selector_all("#search .g")
        for result in search_results:
            title = result.text_content(".LC20lb")
            link = result.get_attribute("href", selector=".r>a")
            results.append({"title": title, "link": link})
        context.close()
        browser.close()
    return results


async def async_search(keyword):
    print(f"keyword: {keyword}")
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://www.google.com")

        title = await page.title()
        print(f"网页标题：{title}")

        # 输入关键词
        await page.fill('textarea[name="q"]', keyword)

        # 点击“Google 搜索”按钮
        await page.click('input[name="btnK"]')

        # 等待搜索结果加载
        await page.wait_for_load_state("networkidle")

        # 获取搜索结果的标题和链接
        search_results = await page.query_selector_all("#search .g")
        search_list = []
        for i, result in enumerate(search_results):
            print(f"搜索结果 {i+1}：")
            # 获取h3标签的文本内容
            h3 = await result.query_selector("h3")
            title_text = await h3.inner_text()
            print(f"标题：{title_text}")
            # 获取a标签的href属性值
            a= await result.query_selector("a")
            link_href = await a.get_attribute("href")
            print(f"链接：{link_href}")
            search_list.append({"title": title_text, "link": link_href})

        await browser.close()
        return search_list

def real_search(keyword):
    print(f"关键词：{keyword}")
    results = asyncio.run(async_search(keyword))
    print(f"搜索结果：{results}")
    return results

def main():
    print(f"start main function ...")
    keyword = "Python教程"
    print(f"关键词：{keyword}")
    # asyncio.run(async_search(keyword))
    results = asyncio.run(async_search(keyword))
    print(f"搜索结果：{results}")

if __name__ == "__main__":
    main()
    print(f"end main function ...")