from time import sleep
import rpyc

from config import app_config

sleep(5)
conn = rpyc.connect("localhost", app_config.rpc_port_map.get(app_config.env), config = {"allow_all_attrs" : True})
c = conn.root

pos_diff = c.get_position_diff()
strategy_pos = pos_diff[0]
account_pos = pos_diff[1]

diff = {}
for k,v in strategy_pos.items():
    if k not in account_pos.keys():
        diff[k] = strategy_pos[k]
    elif strategy_pos[k] != account_pos[k]:
        if (strategy_pos[k] - account_pos[k]) is not 0:
            diff[k] = strategy_pos[k] - account_pos[k]

print("策略持仓与账户真实持仓之差：")
print(diff)
