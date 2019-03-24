#!/usr/bin/python
# -*- coding:utf-8 -*-
from utils import *

try:
    import MySQLdb
    import MySQLdb.cursors
except:
    Log.log_warn("MySQLdb is not installed!")


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
            self.conn = MySQLdb.connect(host=self.__host, user=self.__username, passwd=self.__password,
                                        port=self.__port, cursorclass=MySQLdb.cursors.DictCursor)
            self.cursor = self.conn.cursor()
        except MySQLdb.Error as e:
            Log.log_error('MySql Error %%s' % str(e))

    def has_useless_db(self, dbs=list):
        if self.cursor is None:
            self.connect()
        self.cursor.execute("show databases")
        for data in self.cursor.fetchall():
            if data['Database'] in dbs:
                Log.log_warn("have useless db %s " % data['Database'])

    def has_obsolete_account(self, username=""):
        if self.conn is None:
            self.connect()
        res = self.cursor.execute("SELECT * FROM mysql.user WHERE user='%s'" % username)
        if res > 0:
            Log.log_warn("has obsolete account!")
        else:
            Log.log_pass("has no obsolete account")

    def load_file(self):
        if self.conn is None:
            self.connect()
        res = self.cursor.execute("select load_file('/etc/passwd')")

    def log_status(self, conf=dict):
        if self.conn is None:
            self.connect()
        self.cursor.execute("show variables like '%log%'")
        res = self.cursor.fetchall()
        for data in res:
            key = data['Variable_name']
            val = data['Value']
            if key in conf.keys():
                if val != conf[key]:
                    Log.log_warn('set %s = %s is not safe!' % (key, val))

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
                    Log.log_warn('setting %s = %s is suggested!' % (key, 'N'))
        if not flag:
            Log.log_pass('All the setting are approriate!')

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
                    Log.log_warn('setting %s = %s is suggested!' % (key, 'N'))
        if not flag:
            Log.log_pass('All the setting are appropriate!')

    def close(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.conn is not None:
            self.conn.close()


def run(setting_file_path):
    root = ET.parse(setting_file_path).getroot()
    username = root.find('.//user/username').text
    password = root.find(".//user/password").text
    test = ConfScan(username, password)
    test.connect()
    Log.log_info("Checking useless databases...")
    test.has_useless_db(dbs={'test', 'mysql', 'information_schema'})
    Log.log_info("Checking useless or abandoned users...")
    test.has_obsolete_account("")
    Log.log_info("Checking if the local file of databases is encrypted...")
    test.load_file()
    Log.log_info("Checking log settings...")
    log_conf = dict()
    log_conf_dom = root.find(".//conf/log")
    for item in log_conf_dom:
        key = item.find('./key').text
        val = item.find('./val').text
        log_conf[key] = val
    test.log_status(log_conf)
    Log.log_info('Check selected user privilege (1/2)...')
    test.check_user_grants('test')
    Log.log_info('Check selected user privilege (2/2)...')
    test.check_user_db_grants('test')


if __name__ == '__main__':
    run("conf.xml")
