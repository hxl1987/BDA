import json, sys, os, re
from Logger import Log
import xml.etree.ElementTree as ET
import ConfigParser
import argparse
import ipaddress

password_regex = re.compile('^.*(?=.{6,16})(?=.*\d)(?=.*[A-Z])(?=.*[a-z]{2,})(?=.*[!@#$%^&*?\(\)]).*$')


def check_pwd(pwd):
    if password_regex.match(pwd):
        return 1
    return 0


def is_ip_internal(ip):
    try:
        return ipaddress.ip_address(ip).is_private
    except:
        return False
