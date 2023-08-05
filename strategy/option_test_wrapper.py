from time import sleep
from vnpy.app.script_trader import ScriptEngine
import datetime as dt

import sys
sys.path.append('C:\\Users\\Administrator\\Desktop\\trade\\tradeStrategy\\Option_new\\option_factor')
sys.path.append('C:\\Users\\Administrator\\Desktop\\trade')
# sys.path.append('C:\\strategies\\option_strategies')

from option_factor import option_factor
from TQuant.Trade.RedisData import RedisConnector


def run(engine: ScriptEngine):
    today = int(dt.date.today().strftime(('%Y%m%d')))
    RC_bar = RedisConnector(db_name='option_bar')
    params_dict = {
        'subject': '50ETF_option',
        'realTimeTradedate': today,
        'vnpyEngine': engine,
        'data_connector': RC_bar,
    }
    strategy = engine.strategy_object["option_factor.py"] = option_factor(**params_dict)
    strategy.run()