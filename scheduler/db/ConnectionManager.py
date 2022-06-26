import pymysql
import os

class ConnectionManager:

    def __init__(self):
        self.host = os.getenv("Host")
        self.database = os.getenv("DBName")
        self.user = os.getenv("UserID")
        self.password = os.getenv("Password")
        self.conn = None

    def create_connection(self):
        try:
            self.conn = pymysql.connect(host=self.host,
                                        user=self.user,
                                        password=self.password,
                                        database=self.database)
        except pymysql.Error as db_err:
            print("Database Programming Error in SQL connection processing! ")
            print(db_err)
            quit()
        return self.conn

    def close_connection(self):
        try:
            self.conn.close()
        except pymysql.Error as db_err:
            print("Database Programming Error in SQL connection processing! ")
            print(db_err)
            quit()
