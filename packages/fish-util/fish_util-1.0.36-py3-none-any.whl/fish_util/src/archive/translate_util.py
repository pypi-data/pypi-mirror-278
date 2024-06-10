import openai
import re

import lib.openai_util as openai_util

# 定义翻译函数
def translate(text):
    # 判断输入文本是中文还是英文
    if re.match("[\u4e00-\u9fa5]+", text):
        # 中文翻译为英文
        print("中文翻译为英文",text)
        prompt=f"翻译：{text}\n中文翻译为英文："
    else:
        # 英文翻译为中文
        print("英文翻译为中文",text)
        prompt=f"翻译：{text}\n英文翻译为中文："
    api_key="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"
    session = openai_util.Chat(api_key=api_key, model="gpt-3.5-turbo")
    result=session.request(prompt)
    return result

# 测试
# print(translate("你好")) # Hello
# print(translate("Hello")) # 你好
