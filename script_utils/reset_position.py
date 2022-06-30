
import rpyc

from config import app_config

conn = rpyc.connect("localhost", app_config.rpc_port_map.get(app_config.env), config = {"allow_all_attrs" : True})
c = conn.root

c.reset_position()
print("position reset, please check orders again")

