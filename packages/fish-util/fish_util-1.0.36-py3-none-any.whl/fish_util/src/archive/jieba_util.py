# 我想要统计一个标题列表中的所有标题的词性
# 对属于prop_tags的，统计一下这些词和它的词性，并按频率从高到低排序，记录到一个A文件中
# 对不属于prop_tags的，也统计一下这些词和它的词性，并按频率从高到低排序,记录到一个B文件中
#
# 可以做标签的词性：
# eng 英文文本
# l 习用语
# n 名词
# vn 动名词
# nr 人名
# nz 其他专名
# i 成语
# ns 地名
# nt 机构团体名
# j 简称略语
import jieba.posseg as pseg
from collections import Counter,defaultdict
import os
# from fishyer_helper.database_util import *
from fishyer_helper.file_util import *
prop_tags = ["eng", "l", "n", "vn", "nr", "nz", "i","ns","nt"]

global_map = {}

def test_db_process_titles():
    recent = get_recent_bookmark_titles(-1)
    process_text_list(recent)
    print("done")

def cut_word(text):
    elements = pseg.cut(text)
    result=[]
    for w, f in elements:
        result.append((w, f))
        
    return result

def cut_word(text):
    words = pseg.cut(text)
    return [(w, f) for w, f in words]

# 创建一个 defaultdict 对象，它的默认值是一个空列表
word_dict = defaultdict(list)

def cut_text_list(text_list):
    prop_elements = []
    non_prop_elements = []
    count=0
    for text in text_list:
        print(f"count: {count}")
        count+=1
        elements = cut_word(text)
        for word, flag in elements:
            #记录全局map:word->text_list
            word_dict[word].append(text)
            # if word not in global_map:
            #     li=[text]
            #     global_map[w] = li
            # else:
            #     li=global_map[w]
            #     li.append(text)
            #区分是否是标记的词性
            if flag in prop_tags:
                prop_elements.append((word, flag))
            else:
                non_prop_elements.append((word, flag))
    return prop_elements, non_prop_elements

def process_text_list(text_list):
    # 先进行分词和词性标注
    prop_elements, non_prop_elements = cut_text_list(text_list)
    # 对 prop_elements 和 non_prop_elements 进行计数
    prop_counter = Counter(prop_elements)
    non_prop_counter = Counter(non_prop_elements)
    # 按频次排序
    sorted_prop = sorted(prop_counter.items(), key=lambda x: x[1], reverse=True)
    sorted_non_prop = sorted(non_prop_counter.items(), key=lambda x: x[1], reverse=True)
    # 只保留频次在10以上的
    frequency=0
    filtered_prop = [elem for elem in sorted_prop if elem[1] >= frequency]
    filtered_non_prop = [elem for elem in sorted_non_prop if elem[1] >= frequency]
    # 将过滤后的结果写入到文件中
    write_file("log/cut_word/prop_elements.txt", filtered_prop)
    write_file("log/cut_word/non_prop_elements.txt", filtered_non_prop)
    # 将过滤后的每一个分词文件也写入到文件中
    prop_elements_path = "log/cut_word/prop_elements"
    non_prop_elements_path = "log/cut_word/non_prop_elements"
    if not os.path.exists(prop_elements_path):
        os.makedirs(prop_elements_path)
    if not os.path.exists(non_prop_elements_path):
        os.makedirs(non_prop_elements_path)
    for element, count in filtered_prop:
        if count >= frequency:
            try:
                file_name = os.path.join(prop_elements_path, f"{count}-{element[0]}-{element[1]}.md")
                with open(file_name, "a") as f:
                    f.write(f"\n".join(word_dict[element[0]]))
            except:
                print(f"保存词频文件出错了: {count}-{element[0]}-{element[1]}")
    # for word, count, text in filtered_non_prop:
    #     if count >= frequency:
    #         file_name = os.path.join(non_prop_elements_path, f"{word}.md")
    #         with open(file_name, "a") as f:
    #             f.write(f"{count}. {text}\n")

# 请帮我分析上述代码，帮我根据需求补全代码：
# 现在每一个分词都有一个频次，我还想将这个分词所在的text也记录下来，写入到一个cut_elements文件夹中,文件名为分词，内容为text列表的md有序列表格式，如下(忽略# )：
# Flutter.md
# 1. Flutter samples
# 2. Tags - 贾鹏辉的技术博客官网|CrazyCodeBoy|Devio|专注移动技术开发(Android IOS)、Flutter开发、Flutter教程、React Native开发、React Native教程、React Native博客
# 3. Flutter 核心技术与实战
# 4. Flutter 完全手册 - 小德_Kurt - 掘金小册


def test_mock_process_titles():
    # mock_list = [
    #     "我爱自然语言处理",a
    #     "10 分钟搭建自己的专属 ChatGPT",
    #     "源码学习时间，Window Manager in Android",
    #     "CoordinatorLayout驾轻就熟，不怕UI任意需求",
    #     "Flutter 系列（九）：GetX 状态管理核心源码分析",
    #     "布局性能优化：安卓开发者不可错过的性能优化技巧",
    #     "程序员35岁不是坎，是一把程序员自己设计的自旋锁",
    #     "Android稳定性：可远程配置化的Looper兜底框架",
    #     "Linux 编程之信号篇：异常监控必知必会",
    # ]
    content=read_file("data/workflowy/root_2023_10_19.txt")
    mock_list=content.split("\n")
    print(f"mock_list: {len(mock_list)}")
    process_text_list(mock_list)

def write_file(filename, word_list):
    with open(filename, "w", encoding="utf-8") as f:
        for word, count in word_list:
            f.write(f"{word}: {count}\n")





# test_db_process_titles()

test_mock_process_titles()