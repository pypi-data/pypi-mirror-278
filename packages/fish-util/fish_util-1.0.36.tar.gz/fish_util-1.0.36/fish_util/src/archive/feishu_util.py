import requests

def sendMessageToFeishu(message):
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/b82250ce-23e0-4874-b539-da9370a923cf"
    payload = json.dumps({
    "msg_type": "text",
    "content": {
        "text": "hello feishu from flask"
    }
    })
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


print("-------------------[test feishu util]-------------------")
sendMessageToFeishu("hello feishu")