import pandas as pd
import json
import math
from datetime import datetime, timedelta


def compareVariable(backtest_log_path, prod_log_path):
    backtest_data = pd.read_csv(backtest_log_path, header=0)
    prod_data = pd.read_csv(prod_log_path, header=0)
    backtest_data = backtest_data.filter(["Unnamed: 0","10004351"])
    prod_data = prod_data.loc[prod_data['Unnamed: 0'] == "10004351.SSE"]

    print(prod_data) #tv=-0.203,0.221,063


backtest_log_folder = "C:\\data\\backtest_position\\log20220812\\"
backtest_folder = "C:\\data\\backtest_position\\"
prod_log_folder = "C:\\strategies\\"

# compareVariable(backtest_log_folder + "factor2.csv", prod_log_folder + "2022-08-12_factor2_daily.csv")
# compareVariable(backtest_log_folder + "factor1.csv", prod_log_folder + "2022-08-12_factor1_daily.csv")
# compareVariable(backtest_log_folder + "iv2.csv", prod_log_folder + "2022-08-12_iv2_daily.csv")
# compareVariable(backtest_log_folder + "iv1.csv", prod_log_folder + "2022-08-12_iv_daily.csv")
#
# compareVariable(backtest_log_folder + "time_value.csv", prod_log_folder + "2022-08-12_timevalue_daily.csv")

def compareVariableIv2(backtest_log_path, prod_log_path,variable_name):
    backtest_data = pd.read_csv(backtest_log_path, header=0)
    prod_data = pd.read_csv(prod_log_path, header=0)
    backtest_data = backtest_data.filter(["Unnamed: 0","10004025"])
    prod_data = prod_data.loc[prod_data['Unnamed: 0'] == "10004025.SSE"]
    format = "%Y-%m-%d %H:%M:%S.%f"


    for (columnName, columnData) in prod_data.iteritems():

        if '2022' in columnName:
            prod_timestamp = str(datetime.strptime(columnName, format).replace(second=0).replace(microsecond=0)+ timedelta(minutes=0))
            backtest = backtest_data[backtest_data['Unnamed: 0'] == prod_timestamp]
            prod_value = columnData.values[0]
            if backtest['10004025'].values.size >0 :
                backtest_value = backtest['10004025'].values[0]
            else:
                continue
            print(prod_timestamp+" "+variable_name+" prod:"+str(round(prod_value, 5))+" backtest:"+str(round(backtest_value, 5))+" diff:"+str(round(prod_value-backtest_value, 5)))
            # print(prod_timestamp +"    " +variable_name  + " diff:"+str(round(prod_value-backtest_value, 5)))

print("symbol:10004025")
compareVariableIv2(backtest_folder+"iv2_0.csv",prod_log_folder+"2022-09-08_iv2_0_daily.csv","iv2_0.csv")
compareVariableIv2(backtest_folder+"iv2_1.csv",prod_log_folder+"2022-09-08_iv2_1_daily.csv","iv2_1.csv")
compareVariableIv2(backtest_folder+"iv2_2.csv",prod_log_folder+"2022-09-08_iv2_2_daily.csv","iv2_2.csv")
compareVariableIv2(backtest_folder+"iv2_3.csv",prod_log_folder+"2022-09-08_iv2_3_daily.csv","iv2_3.csv")
compareVariableIv2(backtest_folder+"iv2_4.csv",prod_log_folder+"2022-09-08_iv2_4_daily.csv","iv2_4.csv")

compareVariableIv2(backtest_folder+"iv2_0.csv",prod_log_folder+"2022-09-06_iv2_0_daily.csv","iv2_0.csv")
compareVariableIv2(backtest_folder+"iv2_1.csv",prod_log_folder+"2022-09-06_iv2_1_daily.csv","iv2_1.csv")
compareVariableIv2(backtest_folder+"iv2_2.csv",prod_log_folder+"2022-09-06_iv2_2_daily.csv","iv2_2.csv")
compareVariableIv2(backtest_folder+"iv2_3.csv",prod_log_folder+"2022-09-06_iv2_3_daily.csv","iv2_3.csv")
compareVariableIv2(backtest_folder+"iv2_4.csv",prod_log_folder+"2022-09-06_iv2_4_daily.csv","iv2_4.csv")

# df = pd.read_csv("C:\\data\\backtest_position\\position20220812.csv",header=0)
# with open("C:\\data\\position_log\\prod\\2022-08-12.csv", 'r') as file_object:
#     strategy_position = file_object.readlines()
#     for line in strategy_position:
#         timestamp = str(line).split("@")[1].strip()
#         pos = eval((str(line)).split("@")[0])
#         total = 0
#         error = 0
#         for strategy,positions in pos.items():
#             for symbol, position in positions.items():
#                 symbol = symbol.replace(".SSE", "")
#                 format = "%Y-%m-%d %H:%M:%S"
#                 backtest_timestamp = str(datetime.strptime(timestamp, format).replace(second=0) + timedelta(minutes=1))
#                 backtest = df[df['trade_datetime'] == backtest_timestamp]
#                 if symbol in backtest:
#                     if backtest[symbol].values.size > 0:
#                         if math.copysign(1.0, backtest[symbol].values[0]) != math.copysign(1.0,position):
#                             print(symbol + " backtest position:" +str(backtest[symbol].values[0]) + " strategy position:" +str(position))
#                             error += 1
#                         if position != 0.0 or backtest[symbol].values[0]!= 0.0:
#                             total += 1
#
#             print(timestamp + "error rate:")
#             if total > 0 :
#                 print(error / total)
