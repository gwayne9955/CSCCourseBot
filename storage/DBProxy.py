import pymysql


class DBProxy:
    def __init__(self):
        self.connection = self.setup()
        self.cursor = self.connection.cursor()

    @staticmethod
    def setup():
        f = open("credentials.txt")
        credentials = f.read().split(',')
        f.close()
        connection = pymysql.connect(host=credentials[0],
                                     user=credentials[1],
                                     password=credentials[2],
                                     db=credentials[3])
        return connection

    def disconnect(self) -> None:
        self.connection.close()

    def store(self, sql: str, data: tuple) -> str:
        try:
            self.cursor.execute(sql, data)
            result = self.cursor.fetchall()
            self.connection.commit()
            return result
        except:
            self.disconnect()
            raise RuntimeError("Database error, closing connection.")

    def call(self, sql: str) -> str:
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except:
            self.disconnect()
            raise RuntimeError("Database error, closing connection.")
   
    def truncate(self, table: str) -> str:
        try:
            self.cursor.execute("DELETE FROM {}".format(table))
            result = self.cursor.fetchall()
            return result
        except:
            self.disconnect()
            raise RuntimeError("Database error, closing connection.")
