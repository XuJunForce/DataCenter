from asyncio import Server
from fastapi import APIRouter, Query
from serverApi.backup import GetSystemStatusWithCache, get_monitor_status, get_historical_data
router = APIRouter()

@router.get("/serverInfo/backup", tags=["Server"], summary="获取服务器状态", description="获取服务器的CPU、MEM、DISK使用情况")
async def get_server_status():
    return await GetSystemStatusWithCache()

@router.get("/serverInfo/monitor-status", tags=["Server"], summary="获取监控状态", description="获取系统监控的运行状态和数据统计")
def get_monitor_status_info():
    return get_monitor_status()

@router.get("/serverInfo/historical-data", tags=["Server"], summary="获取历史数据", description="获取前N分钟的历史监控数据，默认60分钟")
def get_historical_data_api(minutes: int = Query(60, description="获取前N分钟的数据", ge=1, le=1440)):
    return get_historical_data(minutes)