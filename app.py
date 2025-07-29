from fastapi import FastAPI  
from fastapi.staticfiles import StaticFiles
import asyncio

#路由
from AI_API.home import router as apiRouter
from serverApi.home import router as serverRouter

#配置信息
from config import Config 


from fastapi.templating import Jinja2Templates
from fastapi import Request
import os


app = FastAPI(
    title="DataCenter API",
    description="数据中心管理系统API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(apiRouter)
app.include_router(serverRouter)

# 创建配置实例
config = Config()

templates = Jinja2Templates(directory=os.path.join(os.getcwd(), "static", "Templates"))

app.mount("/static", StaticFiles(directory=config.staticDir), name="resource")



@app.get("/", tags=["页面"], summary="首页", description="返回系统首页")
def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


