#!/usr/bin/python
# -*- coding: utf-8 -*-
from utils import *


class RedisCheck(object):

    def __init__(self, conf_file):
        self.conf_file = conf_file
        self.conf_content = None
        self.read_content()
        self.combine_include()

    def read_content(self):
        try:
            fp = open(self.conf_file)
            self.conf_content = fp.read()
            fp.close()
        except:
            Log.log_error("Redis Error")
            sys.exit(0)

    def ip_extraction(self):
        ip_re = re.compile("((# |)bind (.+?)\.(.+?)\.(.+?)\.(.+))")
        temp_result = []
        for i in ip_re.findall(self.conf_content):
            if i[0][0] != "#":
                temp_result.append(i[0].replace("bind ", ""))
        return temp_result

    def password_extraction(self):
        password_re = re.compile("((# |)requirepass (.+))")
        temp_result = []
        for i in password_re.findall(self.conf_content):
            if i[0][0] != "#":
                temp_result.append(i[0].replace("requirepass ", ""))
        return temp_result

    def config_extraction(self):
        config_re = re.compile("((# |)rename-command (.+) (.+))")
        temp_result = {}
        for i in config_re.findall(self.conf_content):
            if i[0][0] != "#":
                temp_result[i[2].lower()] = i[3]
        return temp_result

    def add_file(self, file_path):
        try:
            fp = open(file_path)
            self.conf_content += "\n"
            self.conf_content += fp.read()
            fp.close()
        except:
            Log.log_warn("Include file %s cannot be found" % file_path)
            sys.exit(0)

    def combine_include(self):
        include_re = re.compile("((# |)include (.+).conf)")
        for i in include_re.findall(self.conf_content):
            try:
                if i[0][0] != "#":
                    self.add_file(i[2])
            except:
                pass

    def check_exposure(self):
        try:
            ip = self.ip_extraction()[0]
        except:
            Log.log_error("No IP is extracted from config file. Is the config file correct?")
            sys.exit(0)
        if "127.0.0.1" == ip:
            Log.log_pass("Redis is only accessible on this computer")
        elif is_ip_internal(ip):
            Log.log_pass("Redis is only accessible to internal user")
        else:
            Log.log_warn("Redis is set to be exposed to internet, "
                         "try setting 'bind [internal_ip]' in config file")

    def check_password_setting(self):
        if not len(self.password_extraction()):
            Log.log_error("No password has been set, "
                          "try setting 'requirepass [your_password]' in config file")
            return 0
        password = self.password_extraction()[0]
        if check_pwd(password):
            Log.log_pass('Password is strong')
        else:
            Log.log_warn('Password is weak')

    def check_command(self):
        rename_settings = self.config_extraction()
        if "config" not in rename_settings:
            Log.log_warn('Config command is exposed every login user, '
                         'try renaming this command')
        else:
            if check_pwd(rename_settings['config']) or rename_settings['config'] == '""':
                Log.log_pass('Config command is protected strongly')
            else:
                Log.log_warn('Config command is protected weakly'
                             'try using a new name to rename config command')
        if "flushall" not in rename_settings:
            Log.log_warn('Flushall command is exposed to every login user, '
                         'try renaming this command')
        else:
            if check_pwd(rename_settings['flushall']) or rename_settings['flushall'] == '""':
                Log.log_pass('Flushall command is protected strongly')
            else:
                Log.log_warn('Flushall command is protected weakly, '
                             'try using a new name to rename flushall command')
        if "flushdb" not in rename_settings:
            Log.log_warn('Flushdb command is exposed to every login user, '
                         'try renaming this command')
        else:
            if check_pwd(rename_settings['flushdb']) or rename_settings['flushdb'] == '""':
                Log.log_pass('Flushdb command is protected strongly')
            else:
                Log.log_warn('Flushdb command is protected weakly, '
                             'try using a new name to rename flushdb command')


def run(conf_path):
    conf_file = os.path.join(conf_path, 'redis.conf')
    test = RedisCheck(conf_file)
    Log.log_info("Checking exposure...")
    test.check_exposure()
    Log.log_info("Checking setting of password...")
    test.check_password_setting()
    Log.log_info("Checking commands...")
    test.check_command()


if __name__ == "__main__":
    run("/etc/redis")
