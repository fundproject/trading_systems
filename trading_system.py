import datetime
from io import StringIO

import pandas as pd
from vnpy.app.script_trader import init_cli_trading
from vnpy.gateway.uft import UftGateway
from time import sleep
import os
import rpyc
from rpyc.utils.server import ThreadedServer
from threading import Thread
import datetime

from vnpy.trader.constant import Direction, Offset, OrderType

from config import app_config
from config import log_config
from log_utils.logging_utils import log_trades, log_orders, log_positions, log_ticks, log_contracts


class TradingSystem():
    env = app_config.env
    uft_setting = app_config.setting_map.get('uft_'+env)
    ctp_setting = app_config.setting_map.get('ctp_'+env)

    system_configs = app_config.system_configs

    def run(self, strategies):
        self.engine = init_cli_trading([UftGateway])
        self.engine.connect_gateway(self.uft_setting, "UFT")
        # self.engine.connect_gateway(self.ctp_setting, "CTP")

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
                self.engine.map_underlying_symbol()
                for key, value in self.engine.strategy_object.items():
                    if "factor" in key:
                        # only save once for all option strategies
                        self.save_volume(value)
                        self.save_lastest_tick(value)
                # log ticks
                log_ticks(log_config.tick_log_path, self.engine)
                # log trades
                log_trades(log_config.trade_log_path, self.engine)
                # log orders
                log_orders(log_config.order_log_path, self.engine)
                # log positions
                log_positions(log_config.position_log_path, self.engine)
                # log contracts
                log_contracts(log_config.contract_log_path, self.engine)

                self.engine.close()
                exit(0)

            sleep(self.system_configs["trading_min_interval"])

    @staticmethod
    def save_lastest_tick(strategy):
        for key, path in strategy.lastest_tick_path_dict.items():
            last_tick = strategy.lastest_tick[key]
            if last_tick is not None:
                last_tick.to_csv(path)
                last_tick.to_csv(os.path.join(strategy.lastest_tick_dir,
                                              'lastest_{}_tick{}.csv'.format(key, datetime.datetime.today().strftime('%Y-%m-%d'))))

    @staticmethod
    def save_volume(strategy):
        for key, path in strategy.lastest_tick_path_dict.items():
            if key is 'subject':
                last_tick = strategy.lastest_tick[key]
                if last_tick is not None:
                    symbols = "date," + ','.join(list(last_tick.index.values))
                    volumes = datetime.datetime.today().strftime('%Y-%m-%d') + "," + ','.join(
                        str(v) for v in last_tick["volume"])
                    csv = symbols + "\n" + volumes
                    last_vol = pd.read_csv(StringIO(csv))
                    pd.read_csv('C:\\last_volume\\{}\\volume.csv'.format(strategy.env), low_memory=False) \
                        .append(last_vol).to_csv('C:\\last_volume\\{}\\volume.csv'.format(strategy.env), index=False)

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
        # for key, value in self.engine.strategy_object.items():
        #     print("reset position for ", key)
        #     for symbol in value.position.index:
        #         value.set_position(symbol, value.position[symbol])
        #         print("reset position of ", symbol, "to :", value.position[symbol])

        # manually call merge_and_trade for reset position
        self.engine.merge_and_trade()

    def get_contract_info(self):
        contract_info = self.engine.get_all_contracts(True)
        return contract_info

    def test_log(self):
        log_positions(log_config.position_log_path, self.engine)

    def buy_test(self, vt_symbol, volume):
        buy_price = self.engine.get_buy_max_price(vt_symbol)
        print("FOK：")
        self.engine.send_order(vt_symbol, buy_price, volume, Direction.LONG, Offset.OPEN, OrderType.FOK)
        sleep(2)
        print("FAK：")
        # self.engine.send_order(vt_symbol, buy_price, volume, Direction.LONG, Offset.OPEN, OrderType.FAK)
        sleep(2)
        print("MARRKET：")
        self.engine.send_order(vt_symbol, volume, Direction.LONG, Offset.OPEN, OrderType.MARKET)
        sleep(2)
        print("LIMIT：")
        self.engine.send_order(vt_symbol, buy_price, volume, Direction.LONG, Offset.OPEN, OrderType.LIMIT)

class MyService(rpyc.Service):
    def exposed_get_position_diff(self):
        return main.get_position_diff()

    def exposed_reset_position(self):
        main.reset_position()

    def exposed_test_log(self):
        main.test_log()

    def exposed_buy_test(self, vt_symbol, volume):
        main.buy_test(vt_symbol, volume)

    def exposed_get_contract_info(self):
        return main.get_contract_info()



# start the rpyc server
server = ThreadedServer(MyService, port=app_config.rpc_port_map.get(app_config.env),
                        protocol_config={"allow_all_attrs": True})
t = Thread(target=server.start)
t.daemon = True
t.start()
# the main logic
main = TradingSystem()
main.run(app_config.running_strategies)
