from time import sleep
from vnpy.app.script_trader import ScriptEngine
from os import path
import sys
sys.path.append('C:\\strategies\\')
from strategy1 import Strategy

def run(engine: ScriptEngine):
    option_strategy = engine.strategy_object["strategy1.py"] = Strategy()
    option_strategy.run(engine)
