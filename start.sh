source DataCenter_Venv/bin/activate
#启动服务
nohup uvicorn app:app \
    --host 0.0.0.0 \
    --port 13833 \
    --reload \
    > Log/app.log 2>&1 &
