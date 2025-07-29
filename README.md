# DataCenter 仪表盘系统

## 项目概述

这是一个基于FastAPI和Chart.js的数据中心仪表盘系统，提供了用户统计、任务监控、代码分析等功能的可视化界面。

## 技术栈

- **后端**: FastAPI (Python)
- **前端**: HTML5 + CSS3 + JavaScript
- **图表库**: Chart.js 3.9.1
- **模板引擎**: Jinja2Templates

## 页面结构分析

### 1. 页面布局

```
┌─────────────────────────────────────────────────────────┐
│                    Header (64px)                        │
│  Logo + Breadcrumb                    Download Button   │
├─────────────┬───────────────────────────────────────────┤
│             │                                           │
│   Sidebar   │              Main Content                 │
│   (200px)   │                                           │
│             │  ┌─────────────────────────────────────┐  │
│             │  │            Tabs                      │  │
│             │  └─────────────────────────────────────┘  │
│             │  ┌─────────────────────────────────────┐  │
│             │  │         Dashboard Grid              │  │
│             │  │  ┌─────┐ ┌─────────────┐           │  │
│             │  │  │Metric│ │   Chart     │           │  │
│             │  │  └─────┘ └─────────────┘           │  │
│             │  └─────────────────────────────────────┘  │
│             │                                           │
└─────────────┴───────────────────────────────────────────┘
```

### 2. 主要组件

#### Header 组件
- **Logo**: Monkey Code 品牌标识
- **Breadcrumb**: 导航路径显示
- **Download Button**: 客户端下载按钮

#### Sidebar 组件
- **仪表盘**: 当前页面
- **对话记录**: 聊天历史
- **补全记录**: 代码补全历史
- **代码安全**: 安全检查
- **模型管理**: AI模型配置
- **用户管理**: 用户权限管理
- **管理员**: 系统管理
- **帮助文档**: GitHub和交流群

#### Main Content 组件
- **Tabs**: 全局统计 / 成员统计
- **Dashboard Grid**: 12列网格布局
- **Cards**: 各种数据卡片

### 3. 数据卡片类型

#### Metric Cards (指标卡片)
- **总用户数**: 显示用户总数和禁用用户数
- **活跃用户**: 最近90天活跃用户趋势图

#### Chart Cards (图表卡片)
- **工作模式-对话任务**: 饼图显示code/auto模式分布
- **编程语言**: 饼图显示各语言使用比例
- **用户贡献榜**: 排行榜显示用户贡献度
- **实时使用情况**: 柱状图显示近60分钟使用情况
- **对话任务**: 折线图显示90天对话任务趋势
- **补全任务**: 折线图显示90天补全任务趋势
- **代码量**: 折线图显示90天代码修改量
- **补全任务采纳率**: 折线图显示采纳率趋势

## 如何添加新接口

### 1. 后端接口添加

在 `app.py` 中添加新的API接口：

```python
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import json

# 创建路由器
api_router = APIRouter(prefix="/api", tags=["数据接口"])

@api_router.get("/dashboard/stats", summary="获取仪表盘统计数据")
async def get_dashboard_stats():
    """获取仪表盘统计数据"""
    return {
        "total_users": 11,
        "disabled_users": 0,
        "active_users_90d": 9,
        "chat_tasks_90d": 22,
        "completion_tasks_90d": 4447,
        "code_lines_90d": 14728,
        "adoption_rate_90d": 0.00
    }

@api_router.get("/dashboard/charts/{chart_type}", summary="获取图表数据")
async def get_chart_data(chart_type: str):
    """获取指定类型的图表数据"""
    chart_data = {
        "active_users": {
            "labels": list(range(1, 31)),
            "data": [8, 9, 7, 10, 11, 9, 8, 10, 12, 9, 8, 7, 9, 10, 11, 8, 9, 10, 7, 8, 9, 10, 11, 8, 9, 7, 10, 11, 9, 8]
        },
        "work_mode": {
            "labels": ["code", "auto"],
            "data": [75, 25]
        },
        "languages": {
            "labels": ["go", "typescript", "python", "html", "markdown"],
            "data": [40, 25, 15, 12, 8]
        }
    }
    
    if chart_type not in chart_data:
        raise HTTPException(status_code=404, detail="图表类型不存在")
    
    return chart_data[chart_type]

@api_router.get("/dashboard/user-rankings", summary="获取用户排行榜")
async def get_user_rankings():
    """获取用户贡献排行榜"""
    return [
        {"rank": 1, "name": "李**", "score": 3659},
        {"rank": 2, "name": "罗**", "score": 3605},
        {"rank": 3, "name": "翻**", "score": 2307},
        {"rank": 4, "name": "王**", "score": 1747},
        {"rank": 5, "name": "丹**", "score": 1332}
    ]

# 在主应用中包含路由器
app.include_router(api_router)
```

### 2. 前端数据获取

在 `index.html` 中添加数据获取函数：

```javascript
// 数据获取函数
async function fetchDashboardData() {
    try {
        const response = await fetch('/api/dashboard/stats');
        const data = await response.json();
        updateDashboardStats(data);
    } catch (error) {
        console.error('获取仪表盘数据失败:', error);
    }
}

async function fetchChartData(chartType) {
    try {
        const response = await fetch(`/api/dashboard/charts/${chartType}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(`获取${chartType}图表数据失败:`, error);
        return null;
    }
}

async function fetchUserRankings() {
    try {
        const response = await fetch('/api/dashboard/user-rankings');
        const data = await response.json();
        updateUserRankings(data);
    } catch (error) {
        console.error('获取用户排行榜失败:', error);
    }
}

// 更新页面数据
function updateDashboardStats(data) {
    document.querySelector('.metric-value').textContent = data.total_users;
    document.querySelector('.metric-desc').textContent = `其中 ${data.disabled_users} 个用户被禁用`;
}

function updateUserRankings(rankings) {
    const rankingList = document.querySelector('.user-rank');
    rankingList.innerHTML = rankings.map(user => 
        `<li><span class="rank-number">${user.rank}</span> <span>${user.name}</span> <span>${user.score}</span></li>`
    ).join('');
}
```

## 如何修改界面内容

### 1. 修改页面标题和品牌

```html
<!-- 修改页面标题 -->
<title>你的系统名称 - 仪表盘</title>

<!-- 修改Logo -->
<div class="logo">你的系统名称</div>
```

### 2. 添加新的侧边栏项目

```html
<div class="sidebar">
    <div class="sidebar-item active">📊 仪表盘</div>
    <div class="sidebar-item">💬 对话记录</div>
    <!-- 添加新项目 -->
    <div class="sidebar-item">📈 新功能</div>
</div>
```

### 3. 添加新的数据卡片

```html
<!-- 在dashboard-grid中添加新卡片 -->
<div class="card metric-card">
    <div class="metric-label">新指标</div>
    <div class="metric-value">123</div>
    <div class="metric-desc">新指标描述</div>
</div>

<div class="card chart-card">
    <div class="card-title">
        新图表
        <span class="time-range">最近 30 天</span>
    </div>
    <div class="chart-container">
        <canvas id="newChart"></canvas>
    </div>
</div>
```

### 4. 添加新的图表

```javascript
// 创建新图表
new Chart(document.getElementById('newChart'), {
    type: 'line', // 或 'bar', 'doughnut', 'pie'
    data: {
        labels: Array.from({length: 30}, (_, i) => i + 1),
        datasets: [{
            data: generateData(30, 100),
            borderColor: '#3b82f6',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            fill: true,
            tension: 0.4
        }]
    },
    options: commonOptions
});
```

## CSS 类名说明

### 布局类
- `.container`: 主容器
- `.sidebar`: 侧边栏
- `.main-content`: 主内容区域
- `.dashboard-grid`: 仪表盘网格布局

### 卡片类
- `.card`: 基础卡片样式
- `.metric-card`: 指标卡片 (span 4)
- `.chart-card`: 图表卡片 (span 8)
- `.full-width`: 全宽卡片 (span 12)
- `.half-width`: 半宽卡片 (span 6)
- `.quarter-width`: 四分之一宽卡片 (span 3)

### 组件类
- `.header`: 页面头部
- `.logo`: Logo样式
- `.sidebar-item`: 侧边栏项目
- `.tab`: 标签页
- `.metric-value`: 指标数值
- `.metric-label`: 指标标签
- `.chart-container`: 图表容器

## 数据格式规范

### 统计数据结构
```json
{
    "total_users": 11,
    "disabled_users": 0,
    "active_users_90d": 9,
    "chat_tasks_90d": 22,
    "completion_tasks_90d": 4447,
    "code_lines_90d": 14728,
    "adoption_rate_90d": 0.00
}
```

### 图表数据结构
```json
{
    "labels": ["标签1", "标签2", "标签3"],
    "data": [数值1, 数值2, 数值3]
}
```

### 用户排行榜结构
```json
[
    {"rank": 1, "name": "用户1", "score": 1000},
    {"rank": 2, "name": "用户2", "score": 800}
]
```

## 部署说明

1. **安装依赖**:
   ```bash
   pip install -r requirements.txt
   ```

2. **启动服务**:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **访问地址**:
   - 主页: http://localhost:8000/index
   - API文档: http://localhost:8000/docs
   - ReDoc文档: http://localhost:8000/redoc

## 注意事项

1. **数据更新**: 当前页面使用模拟数据，实际使用时需要连接真实的数据源
2. **响应式设计**: 页面已适配不同屏幕尺寸
3. **性能优化**: 大量数据时建议使用分页或虚拟滚动
4. **安全性**: 生产环境中需要添加身份验证和权限控制
5. **错误处理**: 建议添加完善的错误处理和用户提示

## 扩展建议

1. **实时数据**: 使用WebSocket实现实时数据更新
2. **数据导出**: 添加图表数据导出功能
3. **主题切换**: 支持深色/浅色主题切换
4. **多语言**: 支持国际化
5. **移动端**: 优化移动端体验 