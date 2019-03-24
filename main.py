#!/usr/bin/python
# -*- coding: utf-8 -*- 
from utils import *


def CheckHadoop(args):
    path = args.confFolder
    if not os.path.exists(path):
        Log.log_error("'%s' is not a dir!" % path)
        sys.exit(0)
    abs_path = os.path.abspath(path)
    import HadoopCheck
    HadoopCheck.run(abs_path)


def CheckSpark(args):
    path = args.confFolder
    if not os.path.exists(path):
        Log.log_error("'%s' is not a dir!" % path)
        sys.exit(0)
    abs_path = os.path.abspath(path)
    import SparkCheck
    SparkCheck.run(abs_path)


def CheckMySQL(args):
    un = args.username
    pw = args.password
    if args.host:
        host = args.host
    else:
        host = "127.0.0.1"
    if args.port:
        port = args.port
    else:
        port = 3306
    import MySQLCheck
    MySQLCheck.run(un, pw, host=host, port=port)


def main():
    parser = argparse.ArgumentParser(
        description="This is a tool for detecting the security problem of spark and hadoop!")
    subparsers = parser.add_subparsers(help='commands')
    # Hadoop
    conf_check_parser = subparsers.add_parser('Hadoop', help='check the security of hadoop')
    conf_check_parser.add_argument('confFolder', action='store', help='the dir of Hadoop configuration files')
    conf_check_parser.set_defaults(func=CheckHadoop)
    # Spark
    setting_check_parser = subparsers.add_parser('Spark', help='Check the security of spark')
    setting_check_parser.add_argument('confFolder', action='store', help='the dir of Spark configuration files')
    setting_check_parser.set_defaults(func=CheckSpark)
    # MySQL
    setting_check_parser = subparsers.add_parser('MySQL', help='Check MySQL database setting')
    setting_check_parser.add_argument('username', action='store', help='the username of MySQL')
    setting_check_parser.add_argument('password', action='store', help='the password of MySQL')
    setting_check_parser.add_argument('--host', nargs='?', action='store', help='the host of MySQL, default: 127.0.0.1')
    setting_check_parser.add_argument('--port', nargs='?', action='store', help='the port of MySQL, default: 3306')

    setting_check_parser.set_defaults(func=CheckMySQL)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
