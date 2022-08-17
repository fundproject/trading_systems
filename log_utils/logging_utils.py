import datetime
import os
import sys
sys.path.append('C:\\strategies\\')
import pandas as pd

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
    outname = datetime.datetime.today().strftime('%Y-%m-%d') + ".csv"
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    fullname = os.path.join(outdir, outname)
    log = ""
    for position in engine.position_log:
        log += str(position) + "\n"
    with open(fullname, 'w') as filetowrite:
        filetowrite.write(log)
    print('log positions')

def log_ticks(outdir, engine):
    symbols = []
    # symbols = engine.universe
    symbols.append("510050.SSE")
    for symbol in symbols:
        result = [str(a) for a in engine.main_engine.get_engine("oms").list if
                  a.vt_symbol == symbol]
        today_tick = "\n".join(result)
        dir = '{}/{}'.format(outdir,symbol)
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
