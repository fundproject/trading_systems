from time import sleep
from vnpy.app.script_trader import ScriptEngine

import sys
sys.path.append('C:\\strategies\\')
from butterfly_spread import strategy


def run(engine: ScriptEngine):
    option_strategy = engine.strategy_object["butterfly_spread.py"] = strategy()
    option_strategy.run(engine)
