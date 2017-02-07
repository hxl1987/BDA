#!/usr/bin/python
# -*- coding: utf-8 -*- 
'''
python mdpt.py PasswordGuess -s 127.0.0.1 -p 3306 -u accounts/user_tiny.list -w accounts/word_tiny.list
python mdpt.py ConfigCheck security.conf
python mdpt.py SettingCheck conf.xml
'''
import argparse
import common

def ConfigCheck(args):
	import ConfigCheck
	ConfigCheck.run(args.confFilePath)

def SettingCheck(args):
	import SettingCheck
	SettingCheck.run(args.settingFilePath)

def GuessPassword(args):
	import PasswordGuess
	PasswordGuess.run(args)

def main():

	parser = argparse.ArgumentParser(description="This is a MySQL database peneration tool")

	subparsers = parser.add_subparsers(help='commands')

	# A ConfigCheck command
	conf_check_parser = subparsers.add_parser('ConfigCheck', help='check conf of database server')
	conf_check_parser.add_argument('confFilePath', action='store', help='the path of configure file(my.cnf or my.ini)')
	conf_check_parser.set_defaults(func=ConfigCheck)
	# A SettingCheck command
	setting_check_parser = subparsers.add_parser('SettingCheck', help='check database setting')
	setting_check_parser.add_argument('settingFilePath', action='store', help='the file which contains the setting you want to check ')
	setting_check_parser.set_defaults(func=SettingCheck)

	# A PasswordGuess command
	pass_guess_parser = subparsers.add_parser('PasswordGuess', help='Guess password of your database server')
	pass_guess_parser.add_argument('-s', dest="server_name", action='store', default=common.DEFAULT_HOST, help='database server address')
	pass_guess_parser.add_argument('-p', dest="server_port", action='store', default=common.DEFAULT_PORT, type=int,help="database server port")
	pass_guess_parser.add_argument('-u', dest="user_list", action='store', default=common.DEFAULT_USER_LIST, help='a list of username')
	pass_guess_parser.add_argument('-w', dest="word_list", action='store', default=common.DEFAULT_WORD_LIST, help='a list of password')
	pass_guess_parser.set_defaults(func=GuessPassword)
	args = parser.parse_args()
	args.func(args)

if __name__ == '__main__':
	main()