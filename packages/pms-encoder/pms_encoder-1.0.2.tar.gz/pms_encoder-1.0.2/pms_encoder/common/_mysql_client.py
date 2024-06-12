import pymysql
import os

class MySQLClient:
    
    def _connect(self):
        self.conn = pymysql.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            db=os.getenv("DB_NAME"),
            charset='utf8',
        )
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        
    def _close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
    
    def execute(self, sql, params=None):
        self._connect()
        self.cursor.execute(sql, params)
        self.conn.commit()
        self._close()
        
    def fetchone(self, sql, params=None):
        self._connect()
        self.cursor.execute(sql, params)
        result = self.cursor.fetchone()
        self._close()
        return result
        
    def fetchall(self, sql, params=None):
        self._connect()
        self.cursor.execute(sql, params)
        result = self.cursor.fetchall()
        self._close()
        return result
            