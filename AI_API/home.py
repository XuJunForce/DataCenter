from AI_API.gptUsage import GetGptUsage
from AI_API.deepseekUsage import GetDeepseekUsage
from fastapi import APIRouter

router = APIRouter()

router.get("/apiUsage", tags=["API"], summary="获取GPT API使用情况", description="获取GPT API Key的使用情况和余额信息")(GetGptUsage)

router.get("/DeepseekApiUsage", tags=["API"], summary="获取DeepSeek API使用情况", description="获取DeepSeek API的使用情况和token余额信息")(GetDeepseekUsage)
