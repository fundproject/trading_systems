from time import sleep
import rpyc

from config import app_config

sleep(5)
conn = rpyc.connect("localhost", app_config.rpc_port_map.get(app_config.env), config = {"allow_all_attrs" : True})
c = conn.root

c.test_log()
print(" ")
