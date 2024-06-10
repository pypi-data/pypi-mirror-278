import pandas as pd,LogUtil

# 解析慕课网-实战课程 https://www.imooc.com/u/index/szcourses/list?page=2
def parseImoocSzCourse():
    path="C:/Users/Administrator/Downloads/imooc (2).csv"
    unsorted_df = pd.read_csv(path)
    # 分割原有字段，增加2列
    unsorted_df['pageId'] = unsorted_df['web-scraper-order'].str.split("-").apply(lambda x: x[0])
    unsorted_df['orderId'] = unsorted_df['web-scraper-order'].str.split("-").apply(lambda x: x[1])
    # 先按pageId降序，再按orderId升序
    sorted_df = unsorted_df.sort_values(by=['pageId','orderId'] ,kind='mergesort',ascending=(False,True))
    # 遍历df
    for index, row in sorted_df.iterrows():
        name=row["title"]
        link=row["title-href"]
        LogUtil.add(f"- {name}")
        LogUtil.add(f"  - [{name}]({link})")
    LogUtil.commit()

# 将WebScraper导出的原始数据，进行排序
def sortWebScraperOrder(unsorted_df):
    # 分割原有字段，增加2列
    unsorted_df['pageId'] = unsorted_df['web-scraper-order'].str.split("-").apply(lambda x: x[0])
    unsorted_df['rowId'] = unsorted_df['web-scraper-order'].str.split("-").apply(lambda x: x[1])
    # 先按pageId降序，再按rowId升序
    sorted_df = unsorted_df.sort_values(by=['pageId','rowId'] ,kind='mergesort',ascending=(False,True))
    return sorted_df

path="C:/Users/Administrator/Downloads/imooc-class.csv"
unsorted_df = pd.read_csv(path)
sorted_df=sortWebScraperOrder(unsorted_df)

for index, row in sorted_df.iterrows():
    name=row["data-name"]
    link=row["data-url"]
    LogUtil.add(f"- {name}")
    LogUtil.add(f"  - [{name}](https:{link})")
LogUtil.commit()