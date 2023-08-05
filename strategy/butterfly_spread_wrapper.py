from time import sleep
from vnpy.app.script_trader import ScriptEngine

import sys
sys.path.append('C:\\Users\\user2\\Desktop\\btc_hft_2020\\tradeStrategy\\Option\\butterfly_spread')
# sys.path.append('C:\\strategies\\option_strategies')

from butterfly_spread import butterfly_spread   


def run(engine: ScriptEngine):
    engine.strategy_object["butterfly_spread_50ETF_option"] = butterfly_spread('50ETF_option', engine)
    engine.strategy_object["butterfly_spread_50ETF_option"].run()

    # engine.strategy_object["butterfly_spread_300ETF_option"] = butterfly_spread('300ETF_option', engine)
    # engine.strategy_object["butterfly_spread_300ETF_option"].run()


    # engine.strategy_object['50ETF_option']["butterfly_spread"] = butterfly_spread('50ETF_option', engine)
    # engine.strategy_object['50ETF_option']["butterfly_spread"].run()
