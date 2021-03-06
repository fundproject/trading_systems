import datetime
from vnpy.app.script_trader import init_cli_trading
from vnpy.gateway.uft import UftGateway
from time import sleep
import os
import rpyc
from rpyc.utils.server import ThreadedServer
from threading import Thread
import datetime

from config import app_config
from config import log_config
from log_utils.logging import log_trades, log_orders, log_positions


class TradingSystem():
    env = app_config.env
    setting = app_config.setting_map.get(env)
    system_configs = app_config.system_configs

    def run(self, strategies):
        self.engine = init_cli_trading([UftGateway])
        self.engine.connect_gateway(self.setting, "UFT")
        sleep(10)
        for strategy in strategies:
            self.engine.start_strategy(strategy)

        while (True):
            if self.time_for_cancel_all():
                self.engine.cancel_all()
            if self.engine.system_trade_flag:
                self.engine.merge_and_trade()
                sleep(self.system_configs["cooldown"])
                print("cooldown")
            # 有序关闭交易系统并写出log
            if datetime.datetime.now().time() > datetime.time(15, 35, 0):
                for key, value in self.engine.strategy_object.items():
                    # for each strategy
                    symbols = value.universe
                    symbols.append("510050.SSE")
                    for symbol in symbols:
                        result = [str(a) for a in self.engine.main_engine.get_engine("oms").list if
                                  a.vt_symbol == symbol]
                        today_tick = "\n".join(result)
                        outdir = 'C:/data/{}'.format(symbol)
                        outname = symbol + "_" + datetime.datetime.today().strftime('%Y-%m-%d') + ".csv"
                        if not os.path.exists(outdir):
                            os.makedirs(outdir)
                        fullname = os.path.join(outdir, outname)
                        f = open(fullname, 'w')
                        f.write(today_tick)
                        f.close()

                    print("log ticks")
                    # log trades
                    log_trades(log_config.trade_log_path, self.engine)
                    # log orders
                    log_orders(log_config.order_log_path, self.engine)
                    # log positions
                    log_positions(log_config.position_log_path.env, self.engine)

                    self.engine.close()
                    exit(0)

            sleep(self.system_configs["trading_min_interval"])

    def time_for_cancel_all(self):
        if self.engine.cancel_all_flag:
            return False
        if datetime.datetime.now().second > self.system_configs["seconds_for_cancel_all"]:
            return True
        return False

    def get_position_diff(self):
        strategies_position = {}
        account_position = {}
        pos = [strategies_position, account_position]
        for key, value in self.engine.strategy_object.items():
            for symbol in value.position.index:
                account_pos = 0
                if self.engine.get_position(symbol + ".多") is not None:
                    account_pos += self.engine.get_position(symbol + ".多").volume
                if self.engine.get_position(symbol + ".空") is not None:
                    account_pos -= self.engine.get_position(symbol + ".空").volume
                account_position[symbol] = int(account_pos)
                if symbol in strategies_position.keys():
                    strategies_position[symbol] += value.position[symbol]
                else:
                    strategies_position[symbol] = value.position[symbol]

        return pos

    def reset_position(self):
        # cancel all active orders
        orders = self.engine.get_all_active_orders()
        for order in orders:
            if order:
                req = order.create_cancel_request()
                self.engine.main_engine.cancel_order(req, order.gateway_name)
        # reset account position to strategy position
        for key, value in self.engine.strategy_object.items():
            print("reset position for ", key)
            for symbol in value.position.index:
                value.set_position(symbol, value.position[symbol])
                print("reset position of ", symbol, "to :", value.position[symbol])


class MyService(rpyc.Service):
    def exposed_get_position_diff(self):
        return main.get_position_diff()

    def exposed_reset_position(self):
        main.reset_position()


# start the rpyc server
server = ThreadedServer(MyService, port=app_config.rpc_port_map.get(app_config.env),
                        protocol_config={"allow_all_attrs": True})
t = Thread(target=server.start)
t.daemon = True
t.start()
# the main logic
main = TradingSystem()
main.run(app_config.running_strategies)
