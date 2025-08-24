import redis

class Memory:
    def __init__(self, user_id):
        self.user_id = user_id
        self.key = f"memory:user:{user_id}"
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def add(self, content):
        self.r.rpush(self.key, content)

    def list(self):
        return [mem.decode() for mem in self.r.lrange(self.key, 0, -1)]

    def delete(self, index):
        # Accept 1-based index from user, convert to 0-based for Redis
        redis_index = index - 1
        if not self.r.exists(self.key):
            return
        self.r.lset(self.key, redis_index, "__DELETED__")
        self.r.lrem(self.key, 1, "__DELETED__")
