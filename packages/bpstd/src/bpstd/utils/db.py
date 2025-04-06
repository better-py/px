from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database


class DBEngine:
    """创建db
    CREATE DATABASE mydatabase CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


    """

    def __init__(self, host, port, user, password, db_name):
        self.host = host
        self.port = port
        #
        self.user = user
        self.password = password
        #
        self.db_name = db_name
        #
        self.db_charset = "utf8mb4"
        self.db_collation = "utf8mb4_unicode_ci"

    @property
    def db_url(self):
        # utf8mb4
        url = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset={5}?collation=utf8mb4_unicode_ci".format(
            self.user,
            self.password,
            self.host,
            self.port,
            self.db_name,
            self.db_charset,
        )
        return url

    @property
    def engine(self):
        connect_args = {
            "init_command": "SET @@collation_connection='utf8mb4_unicode_ci'"
        }
        return create_engine(self.db_url, connect_args=connect_args)

    def conn(self):
        return self.engine.connect()

    def create_db(self):
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
            print("is exist: ", database_exists(self.engine.url))

            # sql_text = """
            #     CREATE DATABASE {0} CHARACTER SET = '{1}' COLLATE = '{2}'
            # """.format(quote(self.engine, self.db_name), self.db_charset, self.db_collation)
            # self.engine.execute(sql_text)
            # conn = self.engine.connect()
            # conn.execute("SET NAMES 'utf8mb4' COLLATE 'utf8mb4_unicode_ci'")
            # print(conn.execute('select @@collation_connection;').fetchall())

    def drop_db(self):
        return drop_database(url=self.engine.url)
