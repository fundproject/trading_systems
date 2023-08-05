import redis
import sys
sys.path.append("C:\\trading_systems\\")
from config import app_config
import uuid

class RedisConnector:
    def __init__(self, db_id=None):
        if db_id is None:
            self.db_id = 0
            if app_config.env == 'prod':
                self.db_id = 1
            elif app_config.env == 'stage':
                self.db_id = 2
        else:
            self.db_id = db_id
        self.pool = redis.ConnectionPool(host='127.0.0.1', db=self.db_id)
        self.redis_config = {
            "tick_scheme": "vt_symbol,last_price,exchange,datetime,volume,turnover,open_interest,last_volume,limit_up,limit_down,open_price,high_price,low_price,pre_close,bid_price_1,bid_price_2,bid_price_3,bid_price_4,bid_price_5,ask_price_1,ask_price_2,ask_price_3,ask_price_4,ask_price_5,bid_volume_1,bid_volume_2,bid_volume_3,bid_volume_4,bid_volume_5,ask_volume_1,ask_volume_2,ask_volume_3,ask_volume_4,ask_volume_5,localtime"
        }
        r = redis.Redis(connection_pool=self.pool)
        self.pipe = r.pipeline()
        
        self.batch_size = 10
        self.queue_count = 0
        self.flush_db()

    def append_tick(self, code, tick):
        try:
            pipe = self.pipe
            attributes = tick.__dict__
            attributes['id'] = uuid.uuid4().hex
            pipe.rpush(code, ",".join(str(v)for v in attributes.values()))
            # print("redis tick")
            # print(",".join(str(v) for v in attributes.keys()))
            self.queue_count += 1
            if self.queue_count % self.batch_size == 0:
                pipe.execute()
                self.queue_count = 0
        except:
            print("redis writting failure")

    def get_ticker_keys(self):
        r = redis.Redis(connection_pool=self.pool)
        return r

    def get_price_list(self, code):
        r = redis.Redis(connection_pool=self.pool)
        return r.lrange(code, 0, -1)

    def get_price_latest(self, code):
        r = redis.Redis(connection_pool=self.pool)
        return r.lrange(code, -1, -1)

    def get_keys(self):
        r = redis.Redis(connection_pool=self.pool)
        return r.keys()

    def flush_db(self):
        r = redis.Redis(connection_pool=self.pool)
        r.flushdb()
        print(app_config.env + " redis db refreshed: " + str(self.db_id))
