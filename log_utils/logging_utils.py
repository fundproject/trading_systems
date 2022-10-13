import datetime
import os
import sys

sys.path.append('C:\\strategies\\')
import pandas as pd
import json


def log_trades(outdir, engine):
    outname = datetime.datetime.today().strftime('%Y-%m-%d') + ".csv"
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    fullname = os.path.join(outdir, outname)
    log = ""
    for k, trade_log in engine.main_engine.engines['oms'].trades.items():
        log += str(trade_log) + "\n"
    with open(fullname, 'w') as filetowrite:
        filetowrite.write(log)
    print('log trades ')


def log_orders(outdir, engine):
    outname = datetime.datetime.today().strftime('%Y-%m-%d') + ".csv"
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    fullname = os.path.join(outdir, outname)
    log = ""
    for k, order_log in engine.main_engine.engines['oms'].orders.items():
        log += str(order_log) + "\n"
    with open(fullname, 'w') as filetowrite:
        filetowrite.write(log)
    print('log orders')


def log_positions(outdir, engine):
    outname = datetime.datetime.today().strftime('%Y-%m-%d') + ".txt"
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    # account position log
    account_position_path = os.path.join(outdir, "account_position_" + outname)
    account_position_log = ""
    for position in engine.system_position_log:
        account_position_log += str(position) + "\n"
    with open(account_position_path, 'w') as filetowrite:
        filetowrite.write(account_position_log)

    # strategy position log
    position_map = {}
    for log in engine.position_log:
        try:
            position_dict = json.loads(r'{}'.format(log.split("@")[0].replace("'", "\"")))
            timestamp = log.split("@")[1]
            for strategy, pos in position_dict.items():
                if strategy not in position_map.keys():
                    position_map[strategy] = []
                position_map[strategy].append(str(pos) + "@" + timestamp)
        except:
            print(log)
    for strategy, pos in position_map.items():
        strategy = strategy.split(".")[0]
        strategy_position_log = ""
        strategy_position_path = os.path.join(outdir + "strategy/" + strategy + "/", strategy + "_" + outname)
        for position in pos:
            strategy_position_log += str(position) + "\n"
        os.makedirs(os.path.dirname(strategy_position_path), exist_ok=True)
        with open(strategy_position_path, 'w') as filetowrite:
            filetowrite.write(strategy_position_log)

    # type/underlying position log
    underlying_symbols_map = engine.underlying_symbols_map  # key: underlying, value : set of symbols
    log_map = {}
    for key in underlying_symbols_map.keys():
        log_map[key] = []
    for position in engine.system_position_log:
        try:
            underlying_map = {}  # underlying -> pos dict at current timestamp
            timestamp = position.split("@")[1]
            pos_dict = json.loads(r'{}'.format(position.split("@")[0].replace("'", "\"")))
            for symbol in pos_dict.keys():
                for underlying, symbols in underlying_symbols_map.items():
                    if symbol in symbols:
                        if underlying not in underlying_map.keys():
                            underlying_map[underlying] = {}
                        underlying_map[underlying][symbol] = pos_dict[symbol]
            for underlying, pos in underlying_map.items():
                log_map[underlying].append(str(pos) + "@" + timestamp)
        except:
            print(position)

    for underlying, logs in log_map.items():
        log_str = ""
        underlying_position_path = os.path.join(outdir + "type/" + underlying + "/", underlying + "_" + outname)
        for position in logs:
            log_str += str(position) + "\n"
        os.makedirs(os.path.dirname(underlying_position_path), exist_ok=True)
        with open(underlying_position_path, 'w') as filetowrite:
            filetowrite.write(log_str)

    print('log positions')


def log_ticks(outdir, engine):
    symbols = ["510050.SSE"]
    # symbols = engine.universe
    for symbol in symbols:
        result = [str(a) for a in engine.main_engine.get_engine("oms").list if
                  a.vt_symbol == symbol]
        today_tick = "\n".join(result)
        dir = '{}/{}'.format(outdir, symbol)
        outname = symbol + "_" + datetime.datetime.today().strftime('%Y-%m-%d') + ".csv"
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        fullname = os.path.join(dir, outname)
        f = open(fullname, 'w')
        f.write(today_tick)
        f.close()
    print("log ticks")


def record_variables(strategy, *args, **kwargs):
    time = datetime.datetime.now()
    if time.minute == 0 and time.hour == 13:
        return
    if time.minute == 30 and time.hour == 11:
        time = time.replace(hour=13, minute=0)
    if time.minute == 30 and time.hour == 9:
        return
    iv = kwargs.get('iv', None)
    iv2 = kwargs.get('iv2', None)
    time_value = kwargs.get('time_value', None)
    price = kwargs.get('price', None)
    factor1 = kwargs.get('factor1', None)
    factor2 = kwargs.get('factor2', None)
    factor = kwargs.get('factor', None)
    unit = kwargs.get('unit', None)

    # for variables recording
    if strategy.iv_daily is None:
        strategy.iv_daily = pd.DataFrame(index=strategy.universe)
    if strategy.iv2_daily is None:
        strategy.iv2_daily = pd.DataFrame(index=strategy.universe)
    if strategy.time_value_daily is None:
        strategy.time_value_daily = pd.DataFrame(index=strategy.universe)
    if strategy.price_daily is None:
        strategy.price_daily = pd.DataFrame(index=strategy.universe)
    if strategy.factor1_daily is None:
        strategy.factor1_daily = pd.DataFrame(index=strategy.universe)
    if strategy.factor2_daily is None:
        strategy.factor2_daily = pd.DataFrame(index=strategy.universe)
    if strategy.ranked_factor_daily is None:
        strategy.ranked_factor_daily = pd.DataFrame(index=strategy.universe)
    if strategy.unit_daily is None:
        strategy.unit_daily = pd.DataFrame(index=strategy.universe)

    if iv is not None:
        strategy.iv_daily[time] = iv
    if iv2 is not None:
        strategy.iv2_daily[time] = iv2
    if time_value is not None:
        strategy.time_value_daily[time] = time_value
    if price is not None:
        strategy.price_daily[time] = price
    if factor1 is not None:
        strategy.factor1_daily[time] = factor1
    if factor2 is not None:
        strategy.factor2_daily[time] = factor2
    if factor is not None:
        strategy.ranked_factor_daily[time] = factor
    if unit is not None:
        strategy.unit_daily[time] = unit
