
import pymysql
from dbutils.pooled_db import PooledDB
from threading import Lock
lock = Lock()

class SQLUtils(object):
    def __init__(self,config):
        if not config:
            raise Exception("config is None")
        self.pool = PooledDB(
            creator=pymysql,  # 使用链接数据库的模块
            maxconnections=0,  # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=0,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            maxcached=0,  # 链接池中最多闲置的链接，0和None不限制
            maxshared=0,  # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的
            blocking=False,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            host = config["host"],
            port = config["port"],
            user = config["user"],
            password = config["password"],
            database = config["database"],
            charset='utf8mb4'
        )
        self.conn = None
        self.cursor = None
    
    def get_con(self):
        conn = self.pool.connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        return conn,cursor

    def close(self,conn=None, cursor=None):
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    def fetch_one(self, sql, args):
        cursor = None
        try:
            _, cursor = self.get_con()
            cursor.execute(sql, args)
            result = cursor.fetchone()
            return result
        except Exception as error:
            print("***fetch_one", error)
        finally:
            self.close(cursor=cursor)

    def fetch_all(self, sql, args):
        cursor = None
        try:
            _, cursor = self.get_con()
            cursor.execute(sql, args)
            result = cursor.fetchall()
            return result
        except Exception as error:
            print("***fetch_all", error)
        finally:
            self.close(cursor=cursor)

    def update(self, sql, args):
        conn, cursor = self.get_con()
        try:
            cursor.execute(sql, args)
            conn.commit()
            return True
        except Exception as error:
            print("***update", error)
            raise error
        finally:
            self.close(conn,cursor)

    def update_all(self, sql, args):
        conn, cursor = self.get_con()
        try:
            cursor.executemany(sql, args)
            conn.commit()
            return True
        except Exception as error:
            print("***update_all", error)
            return False
        finally:
            self.close(conn,cursor)