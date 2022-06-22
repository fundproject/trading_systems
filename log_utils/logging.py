import datetime
import os


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
