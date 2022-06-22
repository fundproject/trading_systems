from pytz import timezone

env = 'stage'  # 系统运行环境， 'stage' 模拟环境 ， 'prod' 实盘环境

running_strategies = ["strategy_wrapper2.py"]  # strategies (wrapper) to be started

prod_setting = {
    "用户名": "300819000012",
    "密码": "199406",
    "行情服务器": "58.246.233.226:20421",  # 实盘行情
    # "行情服务器": "101.230.76.65:20421", #实盘行情
    "交易服务器": "101.230.76.65:20420",  # 实盘交易
    "服务器类型": "ETF期权",
    "产品名称": "",
    "授权编码": "",
    "委托类型": "7"
}

stage_setting = {
    "用户名": "30010074",
    "密码": "199406",
    "交易服务器": "116.236.247.243:21491",  # 模拟交易
    "行情服务器": "116.236.247.243:21492",  # 模拟行情
    "服务器类型": "ETF期权",
    "产品名称": "",
    "授权编码": "",
    "委托类型": "7"
}

setting_map = {'prod': prod_setting, 'stage': stage_setting}
DB_TZ = timezone("Asia/Shanghai")
rpc_port_map = {'prod': 18819, 'stage': 18820}
system_configs = {
    "trading_min_interval": 1,  # 轮询间隔
    "cooldown": 5,  # 两次交易之间的冷却时间
    "seconds_for_cancel_all": 50,  # 每分钟超过50秒取消所有order
}