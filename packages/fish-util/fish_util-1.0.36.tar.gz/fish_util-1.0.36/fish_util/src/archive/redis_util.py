def run():
    print("redis_util.py run")


import redis

# 创建Redis连接
r = redis.Redis(host="localhost", port=6381, password="fish-bared")
