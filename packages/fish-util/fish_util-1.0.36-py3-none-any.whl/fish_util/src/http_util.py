"""
你是Python专家，请你帮我写一个工具文件，要求如下：
1. 用python的requests库写一个网络请求工具类
2. 需要添加日志，打印出请求的curl
3. 需要添加缓存，将response的结果保存为本地文件
4. 需要添加测试文件

测试的curl为：
```
curl 'https://api.dida365.com/api/v2/pomodoros/statistics/generalForDesktop' \
  -H 'authority: api.dida365.com' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'accept-language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7' \
  -H 'cookie: t=43A001113F9610FF7167F5FF96546E0D9211CC7F233E4B604204F7277F28608A70CDC8F9B88343741E1CC8D7C5A7C267B3D3D4BE543F9C28628D28253A247F5C9FFA9776D58ED5D1513ABC6D963F3197F276B1F7BD5918B7BA2928CEE038538345B4A7144E6F42F1DBB847282E80F96F151002FFD8A51141A33160E6335AB9873952CF69E2E8C817E9D7611F5A55A88D9143EE49A1650661F9EBA013E5C2BB6DDFF4AA362A7068F4A781DFC550DC9D9F; AWSALB=fMjvCXXa0e8dIZkUmrEw2lbMdrvPCkHQq+rZ4jv794He4rPlzoF25q7MtoSR6vJVfAi9j0lvrkeBtdLY7ClmgGE5i8faH+xMEpHDoKsH8CBeef7QjtIITz179Xqo; AWSALBCORS=fMjvCXXa0e8dIZkUmrEw2lbMdrvPCkHQq+rZ4jv794He4rPlzoF25q7MtoSR6vJVfAi9j0lvrkeBtdLY7ClmgGE5i8faH+xMEpHDoKsH8CBeef7QjtIITz179Xqo' \
  -H 'hl: zh_CN' \
  -H 'origin: https://dida365.com' \
  -H 'referer: https://dida365.com/' \
  -H 'sec-ch-ua: "Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'traceid: 6544449bc436cd123767721c' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36' \
  -H 'x-device: {"platform":"web","os":"macOS 10.15.7","device":"Chrome 118.0.0.0","name":"","version":5005,"id":"64dc81d2f2210a4a713547f1","channel":"website","campaign":"","websocket":"6543936dc436cd1237676237"}' \
  -H 'x-tz: Asia/Shanghai' \
  --compressed
```


测试的响应数据为：
```
{
    "todayPomoCount": 1,
    "totalPomoCount": 1279,
    "todayPomoDuration": 25,
    "totalPomoDuration": 34291
}
```
"""
import httpx
import py2curl

class CustomClient(httpx.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def request(self, *args, **kwargs):
        print("Before request...")
        response = super().request(*args, **kwargs)
        print("After request...")
        print(f"response.status_code: {response.status_code}")
        print(f"response.json: {response.json}")
        # command = py2curl.render(response.request)
        # print(f"command: {command}")
        return response

client = CustomClient()

response = client.get('http://httpbin.org/get')