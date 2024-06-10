import requests
import hashlib
import json
import random
import re

# 以下参数需要根据你的应用程序进行修改
API_URL = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
APP_ID = '20220530001234260'
SECRET_KEY = 'M_JBtJCp35CDqzm7p09S'

def translate(q):
    is_chinese_pattern = re.compile(r'[\u4e00-\u9fa5]+')
    if is_chinese_pattern.search(q):
        from_lang = 'zh'
        to_lang = 'en' 
    else:
        from_lang = 'en'
        to_lang = 'zh' 
    # print("from_lang:",from_lang)
    # print("to_lang:",to_lang)
    salt = str(random.randint(32768, 65536))
    sign = hashlib.md5((APP_ID + q + salt + SECRET_KEY).encode()).hexdigest()
    params = {
        'q': q,
        'from': from_lang,
        'to': to_lang,
        'appid': APP_ID,
        'salt': salt,
        'sign': sign
    }
    response = requests.get(API_URL, params=params)
    result = json.loads(response.content.decode('utf-8'))
    if result.get('error_code') is None:
        return result['trans_result'][0]['dst']
    else:
        return None

def test_translate():
    chinese_text = '你好'
    english_text = 'hello'

    translated_text1 = translate(chinese_text)
    translated_text2 = translate(english_text)

    print(translated_text1)
    print(translated_text2)

# test_translate()