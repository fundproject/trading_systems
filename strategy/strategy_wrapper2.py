from time import sleep
from vnpy.app.script_trader import ScriptEngine

import sys
sys.path.append('C:\\strategies\\')
from strategy2 import strategy


def run(engine: ScriptEngine):
    option_strategy = engine.strategy_object["strategy_2.py"] = strategy()
    option_strategy.run(engine)
