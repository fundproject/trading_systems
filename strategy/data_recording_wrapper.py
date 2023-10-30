from time import sleep
from vnpy.app.script_trader import ScriptEngine

import sys
sys.path.append('C:\\Users\\user2\\Desktop\\btc_hft_2020\\tradeStrategy\\Option\\data_recording')
# sys.path.append('C:\\strategies\\option_strategies')

from data_recording import data_recording


def run(engine: ScriptEngine):
    strategy = engine.strategy_object["data_recording.py"] = data_recording('50ETF_option', engine)
    strategy.run()