import psycopg2

class DBConnection:

    def __init__(self):
        self.host = 'localhost'
        self.port = 5432
        self.name = 'postgres'
        self.user = 'postgres'
        self.password = '123'
        self.sslmode = None  # Change this to 'verify-ca' if you want to use a CA certificate
        self.sslrootcert = None # path to file ca.pem
        self.conn = None
        self.cursor = None
        self.result = None
        self.connected = False
        self.affected = 0
        self.connect()

    @property
    def connection_status(self):
        return self.connected

    def connect(self):
        try:
            self.conn = psycopg2.connect(host=self.host,
                                        port=self.port,
                                        database=self.name,
                                        user=self.user,
                                        password=self.password,
                                        sslmode=self.sslmode,
                                        sslrootcert=self.sslrootcert)

            self.connected = True
            self.cursor = self.conn.cursor()
        except psycopg2.Error as e:
            self.connected = False
        return self.conn

    def disconnect(self):
        if self.connected:
            self.conn.close()
        else:
            self.conn = None

    def findOne(self, sql):
        self.connect()
        self.cursor.execute(sql)
        self.result = self.cursor.fetchone()
        return self.result

    def findAll(self, sql):
        self.connect()
        self.cursor.execute(sql)
        self.result = self.cursor.fetchall()
        return self.result

    def insert(self, sql, val=None):
        self.connect()
        if val:
            self.cursor.execute(sql, val)
        else:
            self.cursor.execute(sql)
        self.conn.commit()
        self.affected = self.cursor.rowcount
        return self.affected

    def update(self, sql, val=None):
        self.connect()
        if val:
            self.cursor.execute(sql, val)
        else:
            self.cursor.execute(sql)
        self.conn.commit()
        self.affected = self.cursor.rowcount
        return self.affected

    def delete(self, sql, val=None):
        self.connect()
        if val:
            self.cursor.execute(sql, val)
        else:
            self.cursor.execute(sql)
        self.conn.commit()
        self.affected = self.cursor.rowcount
        return self.affected

    def show(self, sql):
        self.connect()
        self.cursor.execute(sql)
        self.result = self.cursor.fetchone()
        return self.result

    @property
    def info(self):
        if self.connected:
            return 'Server is running on ' + self.host + ' using port ' + str(self.port)
        else:
            return 'Server is offline.'
        
a = DBConnection()
b = a.info
print(b)