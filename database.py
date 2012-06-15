import sqlite3

DBNAME = "tempdb.db"
IGNORE_LIST = ["PONG"]

class DB:
    def __init__(self,dbname):
        self.conn = sqlite3.connect(dbname)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS msg ( \
                             id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL , \
                             user TEXT, \
                             command TEXT,  \
                             target TEXT, \
                             message TEXT, \
                             time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

    def __del__(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def read(self):
        return self.cursor.execute("SELECT * FROM msg ORDER BY time ASC").fetchall()

    def write(self, user, data):
        data = data.split(' ')
        if data[0] in IGNORE_LIST: return

        self.cursor.execute("INSERT INTO msg ( user, command , target, message ) VALUES (?, ?, ?, ?)", (user, data[0], data[1], ' '.join(data[2:])))
        self.conn.commit()

client = DB(DBNAME)
