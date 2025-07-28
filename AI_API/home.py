from AI_API.gptUsage import GetGptUsage
from fastapi import APIRouter


router = APIRouter()


router.get("/apiUsage")(GetGptUsage)
