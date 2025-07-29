import httpx
from config import DeepseekConfig

url = "https://platform.deepseek.com/api/v0/users/get_user_summary"

headers = {
    "authorization": DeepseekConfig.auth,
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}

# 单独处理Cookie，避免特殊字符问题
if hasattr(DeepseekConfig, 'cookie') and DeepseekConfig.cookie:
    headers["Cookie"] = DeepseekConfig.cookie

async def GetDeepseekUsage():
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url=url, headers=headers)
            response.raise_for_status()  # 检查HTTP状态码
            
            data = response.json()
            return {
                "APIKEYINFO": data
            }
    except httpx.RequestError as e:
        print(f"请求失败: {e}")
        return {
            "APIKEYINFO": {
                "error": f"请求失败: {str(e)}",
                "balance": 0,
                "used": 0,
                "remaining": 0
            }
        }
    except Exception as e:
        print(f"其他错误: {e}")
        return {
            "APIKEYINFO": {
                "error": f"处理失败: {str(e)}",
                "balance": 0,
                "used": 0,
                "remaining": 0
            }
        }