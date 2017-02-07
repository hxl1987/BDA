#!/usr/bin/python
# -*- coding:utf-8 -*-
import ConfigParser
import sys, getopt, os
from Logger import Log

SECURITY_CONF = "security.conf"

def check_conf(filename):

	security_conf = ConfigParser.SafeConfigParser(allow_no_value=True)
	security_conf.read(SECURITY_CONF)

	check_conf = ConfigParser.SafeConfigParser(allow_no_value=True)
	try:
		check_conf.read(filename)
	except Exception, e:
		Log.log_error ("Failed to parse configure file, please check the file format!")
		sys.exit(0)

	confKV = dict()

	sections = security_conf.sections()

	for section in sections:
		items = security_conf.items(section)
		for item in items:
			key = item[0]
			val = item[1]
			try:
				check_val = check_conf.get(section, key)
			except Exception, e:
				if val != "":
					Log.log_warn ("Suggest to add option:  %s = %s in section [%s]" % (key, val, section))
				else:
					Log.log_warn("Suggest to add option:  %s in section [%s]" % (key, section))
				continue
			if(key == 'port' and int(check_val) == 3306):
				Log.log_warn("Suggest to modify the default port(3306)!")
				continue
			if (val=='' and check_val == None) or (val == check_val):
				if val == '':
					Log.log_pass("Have security setting: %s" % (key))
				else:
					Log.log_pass("Have security setting: %s = %s" % (key, check_val))
			else:
				Log.log_warn("Have Security setting %s, but its value(%s) is not suggested!" % (key, check_val))


def run(config_file_path):
	if not os.path.isfile(config_file_path):
		Log.log_error ('%s doesn`t exists!' % config_file_path)
		sys.exit(0)

	check_conf(config_file_path)

if __name__ == "__main__":

	args = sys.argv[1:]
	if len(args) == 0:
		Log.log_error("Usage: python confOp.py confFilePath")
		sys.exit(0)

	if not os.path.isfile(args[0]):
		Log.log_error ('%s doesn`t exists!' % args[0])
		sys.exit(0)

	check_conf(args[0])

