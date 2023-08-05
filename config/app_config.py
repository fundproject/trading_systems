from pytz import timezone

# 系统运行环境， 'stage' 模拟环境 ， 'prod' 实盘环境
env = "prod"
with open(r'C:/trading_systems/config/env.txt', 'r') as file:
    env = file.read().rstrip()

# running_strategies = ["strategy_wrapper2.py"]  # strategies (wrapper) to be started
# running_strategies = ["option_factor_wrapper.py"]
# running_strategies = ["doublesell_wrapper.py"]
# running_strategies = ["strategy_wrapper2.py", "butterfly_spread_wrapper.py", "doublesell_wrapper.py"]
running_strategies = ["option_factor_wrapper.py", "doublesell_wrapper.py"]
# running_strategies = ["option_test_wrapper.py"]
#
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
ctp_prod_setting = {
    # "用户名": "30010074",
    # "密码": "199406",
    "用户名": "71211519",
    "密码": "681228yxd",
    # "行情服务器": "58.246.233.226:20421", #实盘行情
    "行情服务器": "180.168.212.70:41313",  # 实盘行情
    # "交易服务器": "116.236.247.243:21491", #模拟交易
    "交易服务器": "180.168.212.70:41305",  # 实盘交易
    # "行情服务器": "116.236.247.243:21492", #模拟行情
    "经纪商代码": "8000",
    "产品名称": "client_vnpytest_2.5",
    "授权编码": "PRDCTPZAXMUXPDRC",
}

setting_map = {'uft_prod': prod_setting, 'uft_stage': stage_setting, 'ctp_prod': ctp_prod_setting}
DB_TZ = timezone("Asia/Shanghai")
rpc_port_map = {'prod': 18818, 'stage': 18820}
system_configs = {
    "trading_min_interval": 1,  # 轮询间隔
    "cooldown": 5,  # 两次交易之间的冷却时间
    "seconds_for_cancel_all": 55,  # 每分钟超过50秒取消所有order
}

enabled_underlying = ["510050"]

redis_tick_coloumns = "gateway_name,symbol,exchange,datetime,name,volume,turnover,open_interest,last_price,last_volume,limit_up,limit_down,open_price,high_price,low_price,pre_close,bid_price_1,bid_price_2,bid_price_3,bid_price_4,bid_price_5,ask_price_1,ask_price_2,ask_price_3,ask_price_4,ask_price_5,bid_volume_1,bid_volume_2,bid_volume_3,bid_volume_4,bid_volume_5,ask_volume_1,ask_volume_2,ask_volume_3,ask_volume_4,ask_volume_5,localtime,vt_symbol,id"
