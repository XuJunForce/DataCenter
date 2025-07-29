import requests 
from config import GptKey

# headers = {
#     ":authority": "api.chatanywhere.tech",
#     ":method": "POST",
#     ":path": "/v1/query/balance",
#     ":scheme": "https",
#     "accept": "application/json, text/plain, */*",
#     "accept-encoding": "gzip, deflate, br, zstd",
#     "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
#     "access-control-allow-headers": "Authorization,Origin, X-Requested-With, Content-Type, Accept",
#     "access-control-allow-methods": "GET,POST",
#     "access-control-allow-origin": "*",
#     "authorization": "aaaaaaa",  # 替换成你的真实 token
#     "content-length": "0",
#     "origin": "https://api.chatanywhere.tech",
#     "priority": "u=1, i",
#     "referer": "https://api.chatanywhere.tech/",
#     "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": '"macOS"',
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "same-origin",
#     "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
# }

# 根据method、authority、path结合得到的URL
url = "https://api.chatanywhere.tech/v1/query/balance"
headers = {
    "Authorization": GptKey.api ,
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://api.chatanywhere.tech",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}
def GetGptUsage():
    respond = requests.post(url, headers=headers)
    return{
        "APIKEYINFO":respond.json()
    }
