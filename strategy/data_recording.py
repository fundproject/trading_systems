import os
import numpy as np
import pandas as pd
from scipy import stats

import datetime

import os
import sys
# os.chdir(sys.path[0])
sys.path.append(r'C:\Users\user2\Desktop\btc_hft_2020')

import TQuant as tq
import TQuant.Data as td
from TQuant.Trade.VNPYStrategy import BaseVNPYOptionStrategy
from TQuant.Trade import bsm_imp_vol


class data_recording(BaseVNPYOptionStrategy):

    def stop_signal(self):
        if (self.tradedatetime.hour, self.tradedatetime.minute) >= (15, 31):
            print('Beyond trading time.')
            return True
        else:
            return False

    def before_trade(self):
        super().before_trade()

    def trade_signal(self):
        isTrade = False 
        return isTrade
    
    def trade(self):
        pass

    def after_trade(self):
        pass
        # self.save_record_data(path=r'C:\Users\user2\Desktop\btc_hft_2020\tradeStrategy\Option\option_factor\{}'.format(self.tradedate))
