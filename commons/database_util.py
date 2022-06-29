from sqlite3 import Connection, Cursor
import pymysql

class DatabaseUtil:

    #创建数据库连接
    def create_conn(self):
        self.conn: Connection = pymysql.connect(
            host="localhost",
            user="root",
            password="admin123",
            database="phpwind",
            port=3306
        )
        return self.conn

    #执行SQL语句
    def execute_sql(self,sql):
        # 创建游标
        self.cs: Cursor = self.create_conn().cursor()
        # 通过游标对象执行sql语句
        self.cs.execute(sql)
        #提取值
        value = self.cs.fetchone()
        #关闭连接
        self.close_resouce()
        return value

    #关闭资源
    def close_resouce(self):
        self.cs.close()
        self.conn.close()

if __name__ == '__main__':
    print(DatabaseUtil().execute_sql("select status from pw_user where username='admin'"))