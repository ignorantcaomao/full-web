import sqlite3


class DbOperate:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(DbOperate, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_name):
        self.db_name = db_name
        self.connect = sqlite3.connect(self.db_name)
        self.cursor = self.connect.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connect.close()

    def execute_sql(self, sql):
        try:
            result = self.cursor.execute(sql)
            self.connect.commit()
            return result
        except Exception as e:
            print('execute_sql failed: ', e)
            self.connect.rollback()

    def executemany_sql(self, sql, data_list):
        # example:
        # sql = 'insert into filelist (pkgKey, dirname, filenames, filetypes) values (?, ?, ?, ?);'
        # data_list = [(1, '/etc/sysconfig', 'openshift_option', 'f'), (1, '/usr/share/doc', 'adb-utils-1.6', 'd')]
        try:
            self.cursor.executemany(sql, data_list)
            self.connect.commit()
        except Exception as e:
            self.connect.rollback()
            raise Exception("executemany failed")
