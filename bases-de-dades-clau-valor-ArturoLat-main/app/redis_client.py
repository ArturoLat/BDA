import redis

class RedisClient:
    def __init__(self, host='localhost', port=6379, db=0):
        self._host = host
        self._port = port
        self._db = db
        self._client = redis.Redis(host=self._host, port=self._port, db=self._db)
    
    def close(self):
        self._client.close()

    def ping(self):
        return self._client.ping()

    def set(self, sensor_id, data):
        self._client.set(sensor_id, data)

    def get(self, sensor_id):
        return self._client.get(sensor_id)