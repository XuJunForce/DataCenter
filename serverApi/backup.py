import psutil
import os
import asyncio
from datetime import datetime, timedelta
from pathlib import Path

# 全局变量存储最新的系统状态
_latest_status = None
_last_update_time = None

async def GetSystemStatus():
    # 1. CPU 使用率（1秒内的平均值）
    cpu_percent = psutil.cpu_percent(interval=1)
    
    # 2. 内存使用率
    memory = psutil.virtual_memory()
    memory_total_gb = round(memory.total / (1024 ** 3), 2)  # 总内存（GB）
    memory_used_gb = round(memory.used / (1024 ** 3), 2)    # 已用内存（GB）
    memory_percent = memory.percent                          # 内存使用百分比
    
    # 3. 磁盘使用率（默认获取根分区 "/"）
    disk = psutil.disk_usage('/')
    disk_total_gb = round(disk.total / (1024 ** 3), 2)      # 总磁盘空间（GB）
    disk_used_gb = round(disk.used / (1024 ** 3), 2)        # 已用磁盘空间（GB）
    disk_percent = disk.percent                             # 磁盘使用百分比
    
    return {
        "cpu": {"percent": cpu_percent, "cores": psutil.cpu_count(logical=False)},
        "memory": {
            "total_gb": memory_total_gb,
            "used_gb": memory_used_gb,
            "percent": memory_percent
        },
        "disk": {
            "total_gb": disk_total_gb,
            "used_gb": disk_used_gb,
            "percent": disk_percent
        }
    }

async def _update_system_status():
    """
    更新系统状态并写入文件
    """
    global _latest_status
    
    try:
        # 获取系统状态
        status_data = await GetSystemStatus()
        
        # 更新全局状态
        _latest_status = status_data
        
        # 写入备份文件
        await _write_to_backup_file(
            status_data["cpu"]["percent"],
            status_data["memory"]["used_gb"],
            status_data["memory"]["percent"],
            status_data["disk"]["percent"]
        )
        
        # 格式化时间显示
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"⏰ {current_time} | 📊 系统状态已更新: CPU={status_data['cpu']['percent']}%, MEM={status_data['memory']['percent']}%, DISK={status_data['disk']['percent']}%")
        
    except Exception as e:
        print(f"❌ 更新系统状态时出错: {e}")

async def _write_to_backup_file(cpu_percent, memory_used_gb, memory_percent, disk_percent):
    """
    异步写入备份文件
    """
    try:
        # 确保目录存在
        backup_dir = os.path.join(os.getcwd(), "serverData")
        Path(backup_dir).mkdir(exist_ok=True)
        
        backup_file = os.path.join(backup_dir, "backup.txt")
        
        # 写入数据（包含完整时间戳）
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(backup_file, 'a', encoding='utf-8') as f:
            f.write(f"{current_time}:{cpu_percent}:{memory_used_gb}:{memory_percent}:{disk_percent}\n")
            
    except Exception as e:
        print(f"❌ 写入备份文件时发生异常: {e}")

async def GetSystemStatusWithCache():
    """
    获取系统状态，如果距离上次更新不足1分钟则返回缓存数据
    """
    global _latest_status, _last_update_time
    
    current_time = datetime.now()
    
    # 检查是否需要更新数据（每分钟的整数时间更新）
    should_update = False
    if _last_update_time is None:
        should_update = True
    else:
        # 计算距离上次更新的时间差
        time_diff = current_time - _last_update_time
        # 如果距离上次更新超过1分钟，则更新
        if time_diff.total_seconds() >= 60:
            should_update = True
    
    if should_update:
        await _update_system_status()
        _last_update_time = current_time
    
    return _latest_status

async def start_background_monitor():
    """
    启动后台监控任务，每分钟自动更新系统状态
    """
    print("🔄 系统状态后台监控已启动")
    print("📊 监控频率: 每分钟自动更新")
    print("💾 数据保存: serverData/backup.txt")
    
    while True:
        try:
            # 等待到下一个整数分钟
            now = datetime.now()
            next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
            wait_seconds = (next_minute - now).total_seconds()
            
            if wait_seconds > 0:
                await asyncio.sleep(wait_seconds)
            
            # 更新系统状态
            await _update_system_status()
            
        except Exception as e:
            print(f"❌ 后台监控任务出错: {e}")
            await asyncio.sleep(60)  # 出错时等待1分钟再重试

def get_monitor_status():
    """
    获取监控状态信息
    """
    return {
        "monitor_active": _latest_status is not None,
        "last_update": _last_update_time.isoformat() if _last_update_time else None,
        "data_points": _get_backup_file_count()
    }

def _get_backup_file_count():
    """
    获取备份文件中的数据点数量
    """
    try:
        backup_file = os.path.join(os.getcwd(), "serverData", "backup.txt")
        if os.path.exists(backup_file):
            with open(backup_file, 'r', encoding='utf-8') as f:
                return len(f.readlines())
        return 0
    except Exception:
        return 0

def get_historical_data(minutes=60):
    """
    获取历史数据，默认获取前60分钟的数据
    """
    try:
        backup_file = os.path.join(os.getcwd(), "serverData", "backup.txt")
        if not os.path.exists(backup_file):
            return []
        
        # 计算指定分钟前的时间
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        
        historical_data = []
        with open(backup_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    # 解析数据行：时间戳:CPU:内存使用:内存百分比:磁盘百分比
                    parts = line.split(':')
                    if len(parts) >= 5:
                        # 解析时间戳（格式：2025-07-29 21:49:46）
                        time_str = f"{parts[0]} {parts[1]} {parts[2]}"
                        record_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                        
                        # 只返回指定分钟内的数据
                        if record_time >= cutoff_time:
                            historical_data.append({
                                "timestamp": record_time.strftime("%Y-%m-%d %H:%M:%S"),
                                "cpu": float(parts[3]),
                                "memory_used": float(parts[4]),
                                "memory_percent": float(parts[5]),
                                "disk_percent": float(parts[6])
                            })
                except Exception as e:
                    print(f"解析数据行时出错: {line}, 错误: {e}")
                    continue
        
        # 按时间排序
        historical_data.sort(key=lambda x: x["timestamp"])
        
        # 如果没有指定时间的数据，返回所有可用数据
        if not historical_data:
            print(f"⚠️ 没有找到前{minutes}分钟的数据，返回所有可用数据")
            return get_all_available_data()
        
        print(f"📊 获取到 {len(historical_data)} 条历史数据（前{minutes}分钟）")
        return historical_data
        
    except Exception as e:
        print(f"❌ 获取历史数据时出错: {e}")
        return []

def get_all_available_data():
    """
    获取所有可用的历史数据
    """
    try:
        backup_file = os.path.join(os.getcwd(), "serverData", "backup.txt")
        if not os.path.exists(backup_file):
            return []
        
        historical_data = []
        with open(backup_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    # 解析数据行：时间戳:CPU:内存使用:内存百分比:磁盘百分比
                    parts = line.split(':')
                    if len(parts) >= 5:
                        # 解析时间戳（格式：2025-07-29 21:49:46）
                        time_str = f"{parts[0]} {parts[1]} {parts[2]}"
                        record_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                        
                        historical_data.append({
                            "timestamp": record_time.strftime("%Y-%m-%d %H:%M:%S"),
                            "cpu": float(parts[3]),
                            "memory_used": float(parts[4]),
                            "memory_percent": float(parts[5]),
                            "disk_percent": float(parts[6])
                        })
                except Exception as e:
                    print(f"解析数据行时出错: {line}, 错误: {e}")
                    continue
        
        # 按时间排序
        historical_data.sort(key=lambda x: x["timestamp"])
        print(f"📊 获取到 {len(historical_data)} 条所有可用历史数据")
        return historical_data
        
    except Exception as e:
        print(f"❌ 获取所有历史数据时出错: {e}")
        return []