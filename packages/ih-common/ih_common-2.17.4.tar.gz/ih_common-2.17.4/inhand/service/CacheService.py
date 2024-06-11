from redis import StrictRedis,ConnectionPool,Connection
import sys

sys.path.append('../../')
from inhand.service.SettingService import Redis
from inhand.dto.ErrorException import ErrorCodeException

class CacheService:
    def __init__(self,settings):
        self.settings = settings

    def connect(self):
        pass

    def close(self):
        pass

    def put(self,key,value,expire=None):
        raise (NameError, "Unsupported!")

    def get(self, key):
        raise (NameError, "Unsupported!")

    def exists(self, key):
        raise (NameError, "Unsupported!")

    @staticmethod
    def createCacheService(settings):
        if isinstance(settings,Redis):
            return RedisCacheService(settings)
        else:
            raise (NameError, "Unsupported cache type: {}".format(settings.database.type))

class RedisCacheService(CacheService):

    def __init__(self,settings):
        super().__init__(settings)
        self.cache=StrictRedis(host=settings.host,
                             port=settings.port,
                             db=settings.database,
                             password=settings.password)

    def put(self,key,value,expire=None):
        if expire is not None:
            self.cache.setex(key,expire,value)
        else:
            self.cache.set(key,value)

    def get(self, key):
        if self.exists(key):
            return  self.cache.get(key)
        else:
            raise ErrorCodeException(404,"no such key")

    def exists(self, key):
        return self.cache.exists(key)

class RedisCache(RedisCacheService):
    def __init__(self,cache:StrictRedis):
        self.cache=cache

    def put(self,key,value,expire=None):
        if expire is not None:
            self.cache.setex(key,expire,value)
        else:
            self.cache.set(key,value)

    def get(self, key):
        if self.exists(key):
            return  self.cache.get(key)
        else:
            raise ErrorCodeException(404,"no such key")

    def exists(self, key):
        return self.cache.exists(key)

class RedisPool:
    def __init__(self,settings,max_connections:int):
        self.pool=ConnectionPool(host=settings.host,
                             port=settings.port,
                             db=settings.database,
                             password=settings.password,socket_timeout=30, socket_connect_timeout=30,
                                socket_keepalive=True, encoding='utf-8',health_check_interval=60,
        max_connections=max_connections)

    def get_connection(self):
        return RedisCache(StrictRedis(connection_pool=self.pool))

    def close(self,connnection:StrictRedis):
        self.pool.disconnect(connnection)

"""if __name__ == '__main__':
    pool = RedisPool(host="redis",port=6379,db=2,password="Uxid7apUdks",max_connections=6)

    redis = pool.get_connection()
    redis.set("test","test")
    s = redis.get("test")

    print(s)"""
