#!/usr/bin/python
# -*- coding:utf-8 -*-
from utils import *

try:
    import pymysql
except:
    Log.log_warn("PyMySQL is not installed!")


class ConfScan(object):
    def __init__(self, username, password, host='127.0.0.1', port=3306):
        self.__username = username
        self.__password = password
        self.__host = host
        self.__port = port
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = pymysql.connect(host=self.__host, user=self.__username, passwd=self.__password,
                                        port=self.__port)
            self.cursor = self.conn.cursor()
        except:
            Log.log_error('MySql Error')
            sys.exit(0)

    def check_weak_password(self):
        if check_pwd(self.__password):
            Log.log_pass('Password is strong')
        else:
            Log.log_warn('Password is weak')

    def has_useless_db(self, dbs):
        if self.cursor is None:
            self.connect()
        self.cursor.execute("SHOW DATABASES")
        for data in self.cursor.fetchall():
            if data[0] in dbs:
                Log.log_warn("Have useless DB %s" % data[0])

    def has_obsolete_account(self, username=""):
        if self.conn is None:
            self.connect()
        res = self.cursor.execute("SELECT * FROM mysql.user WHERE user='%s'" % username)
        if res > 0:
            Log.log_warn("Have obsolete account!")
        else:
            Log.log_pass("Have no obsolete account")

    def load_file(self):
        if self.conn is None:
            self.connect()
        try:
            self.cursor.execute("SELECT HEX(LOAD_FILE('/etc/passwd')) INTO DUMPFILE '/tmp/test'")
            Log.log_warn("--secure-file-priv is not enabled")
        except:
            Log.log_pass("--secure-file-priv is enabled")

    def check_user_grants(self, username):
        if self.cursor is None:
            self.connect()
        self.cursor.execute("SELECT Grant_priv, References_priv,Alter_routine_priv,Create_routine_priv,File_priv,"
                            "Create_tmp_table_priv, Lock_tables_priv, Execute_priv,Create_user_priv,Process_priv,"
                            "Reload_priv,Repl_slave_priv, Repl_client_priv, Show_db_priv,Shutdown_priv,Super_priv "
                            "FROM mysql.user "
                            "WHERE User ='%s'" % username)
        result = self.cursor.fetchall()
        flag = 0
        for row in result:
            for key, value in row.items():
                if value == 'Y':
                    flag = 1
                    Log.log_warn('Setting %s = %s is suggested!' % (key, 'N'))
        if not flag:
            Log.log_pass('All the settings are approriate!')

    def check_user_db_grants(self, username):
        if self.cursor is None:
            self.connect()
        self.cursor.execute("SELECT Drop_priv, Grant_priv, References_priv,Create_tmp_table_priv,"
                            "Lock_tables_priv,Create_routine_priv,Alter_routine_priv,Execute_priv,"
                            "Event_priv,Trigger_priv FROM mysql.db "
                            "WHERE User ='%s'" % username)
        res = self.cursor.fetchall()
        flag = 0
        for row in res:
            for key, value in row.items():
                if value == 'Y':
                    flag = 1
                    Log.log_warn('Setting %s = %s is suggested!' % (key, 'N'))
        if not flag:
            Log.log_pass('All the settings are appropriate!')

    def close(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.conn is not None:
            self.conn.close()


def run(un, pw, host="127.0.0.1", port=3306):
    test = ConfScan(un, pw, host, port)
    test.connect()
    Log.log_info("Checking password...")
    test.check_weak_password()
    Log.log_info("Checking useless databases...")
    test.has_useless_db({'test', 'mysql', 'information_schema'})
    Log.log_info("Checking useless or abandoned users...")
    test.has_obsolete_account("")
    Log.log_info("Checking if --secure-file-priv is enabled...")
    test.load_file()
    Log.log_info('Check selected user privilege (1/2)...')
    test.check_user_grants('test')
    Log.log_info('Check selected user privilege (2/2)...')
    test.check_user_db_grants('test')


if __name__ == '__main__':
    run("root", "")
