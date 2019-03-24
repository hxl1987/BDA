import json, sys, os, re
from Logger import Log
import xml.etree.ElementTree as ET
import ConfigParser
import argparse


password_regex = re.compile('^.*(?=.{6,16})(?=.*\d)(?=.*[A-Z])(?=.*[a-z]{2,})(?=.*[!@#$%^&*?\(\)]).*$')


def check_pwd(pwd):
    if password_regex.match(pwd):
        return 1
    return 0
