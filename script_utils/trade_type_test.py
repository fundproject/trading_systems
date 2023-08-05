import time
from time import sleep
import rpyc

from config import app_config


sleep(5)
conn = rpyc.connect("localhost", app_config.rpc_port_map.get("stage"), config = {"allow_all_attrs" : True})
c = conn.root
print("test trade type:")
print(time.time())

c.buy_test("10005192.SSE", 1)


