import redis

def redis_connection():
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        return r
    except Exception as e:
        print("Error: ", e)
        exit(1)