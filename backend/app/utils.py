import pymysql
from dbutils.pooled_db import PooledDB
from pymysql import cursors


POOL = PooledDB(
    creator=pymysql,  # 使用连接数据库的模块
    maxconnections=10,  # 连接池允许最大连接数量，0和null表示不限制连接数
    mincached=2,  # 初始化时，连接池中至少创建的空闲的连接，0表示不创建
    maxcached=5,  # 连接池最多闲置连接，0和null表示不限制
    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。Ture为等待，False为不等待然后报错
    setsession=[],  # 开始会话前执行的命令列表
    ping=0,
    host='localhost', port=3306, user='root', password='123456', db='cguan'
)


def exe_sql(sql, params):
    conn = POOL.connection()
    cursor = conn.cursor(cursor=cursors.DictCursor)
    cursor.execute(sql, params)
    conn.commit()
    cursor.close()
    conn.close()


# 插入数据
def insert(sql, params):
    exe_sql(sql, params)


# 查询数据
def fetch_all(sql):
    conn = POOL.connection()
    cursor = conn.cursor(cursor=cursors.DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


# 搜索
def search_sql(sql, params):
    conn = POOL.connection()
    cursor = conn.cursor(cursor=cursors.DictCursor)
    cursor.execute(sql, params)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def delete(sql, params):
    exe_sql(sql, params)


def put(sql, params):
    exe_sql(sql, params)



