import pandas as pd
import json
import math
from datetime import datetime, timedelta
df = pd.read_csv("C:\\data\\backtest_position\\Option_LongShort_Factor20220908.csv",header=0)
with open("C:\\data\\position_log\\prod\\2022-09-08.csv", 'r') as file_object:
    strategy_position = file_object.readlines()
    for line in strategy_position:
        timestamp = str(line).split("@")[1].strip()
        pos = eval((str(line)).split("@")[0])
        total = 0
        error = 0
        for strategy, positions in pos.items():
            for symbol, position in positions.items():
                symbol = symbol.replace(".SSE", "")
                format = "%Y-%m-%d %H:%M:%S"
                backtest_timestamp = str(datetime.strptime(timestamp, format).replace(second=0) + timedelta(minutes=1))
                backtest = df[df['trade_datetime'] == backtest_timestamp]
                if symbol in backtest:
                    if backtest[symbol].values.size > 0:
                        if math.copysign(1.0, backtest[symbol].values[0]) != math.copysign(1.0,position):
                            print(symbol + " backtest position:" +str(backtest[symbol].values[0]) + " strategy position:" +str(position))
                            error += 1
                        if position != 0.0 or backtest[symbol].values[0]!= 0.0:
                            total += 1

            print(timestamp + "error rate:")
            if total > 0 :
                print(error / total)


