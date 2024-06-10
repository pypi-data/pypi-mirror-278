# import redis
# import pymysql
# from dbutils.pooled_db import PooledDB
# # from DBUtils.PooledDB import PooledDB
# import json
# import pickle

# redis_pool = redis.ConnectionPool(
#     host="127.0.0.1", port=6379, db=0, password="fishyer2850"
# )

# mysql_config = {
#     "host": "127.0.0.1",
#     "user": "root",
#     "password": "fishyer2850",
#     "db": "testdb",
#     "charset": "utf8mb4",
#     "pool_size": 2,
#     "pool_reset_session": True,
#     "connect_timeout": 30,
#     "read_timeout": 30,
#     "write_timeout": 30,
#     "max_allowed_packet": 1024 * 1024 * 32,
# }

# mysql_pool = PooledDB(
#     pymysql,
#     maxconnections=2,
#     host="localhost",
#     user="root",
#     port=3306,
#     passwd="fishyer2850",
#     db="testdb",
#     use_unicode=True,
# )

# # 查询数据库函数
# def query_sql(sql, val):
#     with mysql_pool.connection() as connection:
#         with connection.cursor() as cursor:
#             cursor.execute(sql, val)
#             result = cursor.fetchall()
#             return result


# def real_check_url(url):
#     with mysql_pool.connection() as connection:
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM bookmarks WHERE url=%s", (url,))
#             result = cursor.fetchone()
#             print(f"result: {result}")
#             if result is not None:
#                 # 如果MySQL中存在URL，则将其缓存到Redis中
#                 with redis.Redis(connection_pool=redis_pool) as redis_conn:
#                     redis_conn.set(url, b"1")
#                 return 1
#             else:
#                 return 0


# def real_add_bookmark(title, url):
#     with mysql_pool.connection() as connection:
#         with connection.cursor() as cursor:
#             sql = "INSERT IGNORE INTO bookmarks (title, url) VALUES (%s, %s)"
#             val = (title, url)
#             cursor.execute(sql, val)
#             connection.commit()
#             print(
#                 f"执行SQL完毕，记录的 ID 是:{str(cursor.lastrowid)}",
#             )
#             if cursor.rowcount > 0:
#                 # bf.add(url)
#                 # 在 Redis 中添加书签
#                 with redis.Redis(connection_pool=redis_pool) as redis_conn:
#                     redis_conn.set(url, b"1")
#                 return 1
#             else:
#                 return 0


# def real_delete_bookmark_by_url(url):
#     # 在 MySQL 数据库中删除书签
#     with mysql_pool.connection() as connection:
#         with connection.cursor() as cursor:
#             sql = "DELETE FROM bookmarks WHERE url = %s"
#             val = (url,)
#             cursor.execute(sql, val)
#             connection.commit()
#             print(f"执行 SQL 完毕，受影响的行数是:{str(cursor.rowcount)}")
#             if cursor.rowcount > 0:
#                 # 在 Redis 中删除书签
#                 with redis.Redis(connection_pool=redis_pool) as redis_conn:
#                     redis_conn.delete(url)
#                     print(f"在 Redis 中删除书签 {url}")
#                 return 0
#             else:
#                 return 1


# def real_get_bookmarks(title):
#     bookmarks = []
#     with mysql_pool.connection() as connection:
#         with connection.cursor() as cursor:
#             query = (
#                 "SELECT * FROM bookmarks WHERE title LIKE %s ORDER BY update_time DESC"
#             )
#             print(f"query: {query}")
#             cursor.execute(query, ("%{}%".format(title),))
#             result = cursor.fetchall()
#             for item in result:
#                 bookmark = {"id": item[0], "title": item[1], "url": item[2]}
#                 bookmarks.append(bookmark)
#     print(f"get_bookmarks len: {len(bookmarks)}")
#     return bookmarks


# #


# def real_get_all_bookmarks():
#     bookmarks = []
#     with mysql_pool.connection() as connection:
#         with connection.cursor() as cursor:
#             query = "SELECT * FROM bookmarks ORDER BY update_time DESC"
#             print(f"query: {query}")
#             cursor.execute(query)
#             result = cursor.fetchall()
#             for item in result:
#                 bookmark = {"id": item[0], "title": item[1], "url": item[2]}
#                 bookmarks.append(bookmark)
#     print(f"get_all_bookmarks len: {len(bookmarks)}")
#     return bookmarks


# def get_recent_bookmark_titles(count=100):
#     bookmarks = real_get_all_bookmarks()
#     titles = [bookmark["title"] for bookmark in bookmarks]
#     if count == -1:
#         return titles
#     return titles[:count]


# def save_str(k, v):
#     with redis.Redis(connection_pool=redis_pool) as redis_conn:
#         redis_conn.set(k, v)


# def load_str(k):
#     with redis.Redis(connection_pool=redis_pool) as redis_conn:
#         v = redis_conn.get(k)
#         return v


# # 将Python对象转换为字符串,将字符串保存到Redis中
# def save_obj(k, obj):
#     serialized_obj = pickle.dumps(obj)
#     with redis.Redis(connection_pool=redis_pool) as redis_conn:
#         redis_conn.set(k, serialized_obj)


# # 从Redis中读取字符串，并将其反序列化为Python对象
# def load_obj(k):
#     with redis.Redis(connection_pool=redis_pool) as redis_conn:
#         serialized_obj = redis_conn.get(k)
#         if serialized_obj is None:
#             return None
#         obj = pickle.loads(serialized_obj)
#         print(obj)
#         return obj


# def test_save_obj():
#     obj = {"name": "John", "age": 30}
#     k = "test-obj"
#     save_obj(k, obj)
#     load_obj(k)


# def test_load_str():
#     k = "md/ChromeHistory-2023-03-14.md"
#     json_str = load_str(k)
#     # 将JSON字符串解析为Python对象
#     data = json.loads(json_str)

#     # 将Unicode编码转换为中文字符
#     data = json.loads(json.dumps(data, ensure_ascii=False))

#     # 输出结果
#     # print(data)
#     print(json.dumps(data, ensure_ascii=False, indent=4))


# # test_load_str()
