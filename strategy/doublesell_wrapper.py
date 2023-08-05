from time import sleep
from vnpy.app.script_trader import ScriptEngine

import sys
sys.path.append('C:\\Users\\user2\\Desktop\\btc_hft_2020\\tradeStrategy\\Option\\doublesell')
# sys.path.append('C:\\strategies\\option_strategies')

from doublesell import doublesell


def run(engine: ScriptEngine):
    engine.strategy_object["doublesell.py"]= doublesell('50ETF_option', engine)
    engine.strategy_object["doublesell.py"].run()
