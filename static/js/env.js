// 环境变量配置
window.ENV = {
    // 开发环境
    development: {
        api: {
            baseUrl: 'http://localhost:8000',
            endpoints: {
                usage: '/apiUsage'
            }
        }
    },
    
    // 生产环境
    production: {
        api: {
            baseUrl: 'http://114.132.225.114:13833',
            endpoints: {
                usage: '/apiUsage'
            }
        }
    },
    
    // 测试环境
    test: {
        api: {
            baseUrl: 'http://test-server:8080',
            endpoints: {
                usage: '/apiUsage'
            }
        }
    }
};

// 当前环境（可以通过服务器端注入或手动设置）
window.CURRENT_ENV = 'production'; // 或 'development', 'test'

// 获取当前环境配置
window.getCurrentEnv = function() {
    return window.ENV[window.CURRENT_ENV] || window.ENV.production;
}; 