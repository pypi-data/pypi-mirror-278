import requests
import json

url = "https://www.hulunote.com/myapi/quick-text-put/868253a542864a498090260f2462af3e"

payload = json.dumps({
  "content": "good222333"
})
headers = {
  'Host': 'www.hulunote.com',
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'zh-CN',
  'Content-Type': 'application/json',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'cross-site',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) uTools/2.6.3 Chrome/98.0.4758.141 Electron/17.4.0 Safari/537.36'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
