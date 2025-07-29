// 应用配置文件
window.AppConfig = {
    // API配置
    api: {
        baseUrl: 'http://114.132.225.114:13833',
        endpoints: {
            usage: '/apiUsage'
        },
        refreshInterval: 5 * 1000 * 60 , // 5分钟
        timeout: 10000 // 10秒超时
    },
    
    // 应用信息
    app: {
        title: 'MonkeyCode - 仪表盘',
        version: 'v0.3.0',
        type: '免费版'
    },
    
    // 功能开关
    features: {
        autoRefresh: true,
        showCharts: true,
        enableLogging: true,
        showVersionInfo: true
    },
    
    // UI配置
    ui: {
        theme: 'light',
        language: 'zh-CN',
        timezone: 'Asia/Shanghai',
        chartColors: {
            primary: '#3b82f6',
            secondary: '#10b981',
            warning: '#f59e0b',
            danger: '#ef4444'
        }
    },
    
    // 获取完整的API URL
    getApiUrl: function(endpoint) {
        return this.api.baseUrl + this.api.endpoints[endpoint];
    },
    
    // 获取刷新间隔
    getRefreshInterval: function() {
        return this.api.refreshInterval;
    }
}; 