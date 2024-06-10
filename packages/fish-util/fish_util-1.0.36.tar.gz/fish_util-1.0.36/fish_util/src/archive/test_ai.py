import json

# prompt = """你是数据分析专家，可以总结文字内容，请你根据我给你的文字内容，给我返回一个json数据，json数据的字段有：
# 1. tags: 你总结的这段文字的标签列表
# 2. summary: 你总结的这段文字的内容摘要
# """

# content = """
# 如果只看关系图的话，MVVM与MVP没有什么区别，但实现原理上却不同，MVP通过接口回调的形式，被动的接收Persenter层传递过来的数据。MVVM是以观察者的身份，通过观察数据的变化主动刷新UI。
# """

# resp = """
# {
#   "tags": [
#     "转码经历",
#     "自学编程",
#     "前端开发",
#     "Java后端开发",
#     "实习经历",
#     "学习心路历程"
#   ],
#   "summary": "这篇文章讲述了一个双非非科班普通学生的转码经历。作者通过自学编程，先后接触了深度学习、爬虫、前端开发等多个领域，最终确定了方向，开始学习Java后端开发。在大学期间，作者经历了多次实习，面对挑战和迷茫，最终通过努力找到了理想的工作。整个过程充满坎坷和成长，展现了作者的学习心路历程。"
# }
# """

# data_dict = {"问题": prompt, "示例": resp}
# req_json = json.dumps(data_dict, ensure_ascii=False)
# print(req_json)


resp_data = """{"message": {
        "role": "assistant",
        "content": ""
      }
}
"""

resp_dict = json.loads(resp_data)

content = resp_dict["message"]["content"]
print(content)
