from vnpy.app.script_trader import init_cli_trading
from vnpy.gateway.uft import UftGateway
from time import sleep

import datetime
from config import app_config



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
            if datetime.datetime.now().time() > datetime.time(15, 35, 0):
                self.engine.close()
                exit(0)
            sleep(self.system_configs["trading_min_interval"])


# the main logic
main = TradingSystem()
main.run(["data_recording_wrapper.py"])
