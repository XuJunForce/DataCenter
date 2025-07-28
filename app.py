from fastapi import FastAPI  
from AI_API.home import router as apiRouter

app = FastAPI()

app.include_router(apiRouter)




