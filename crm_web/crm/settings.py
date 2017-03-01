# -*- coding: utf-8 -*-

DEBUG = True
TESTING = False

from datetime import timedelta
import os
import string


SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/crm'
SQLALCHEMY_ECHO = False
SQLALCHEMY_POOL_RECYCLE=3600

SECRET_KEY = r'eequae1cahXitaiquaid0chiecaiNgeith1quoh3quoov5Ohth'
JWT_KEY = 'ojaiw3neibai7esh4Ohmookiaveefahru4ohgheeb9chai8oop4Hu5t'
HTTP_URL = r'http://192.168.1.67:5000/{}?token={}'

PASSWORD_TIME_OUT = 7200

MYSQL_HOST = "127.0.0.1"
MYSQL_USER = "root"
MYSQL_PASS = ""
MYSQL_DB = 'phone'

MAIL_SERVER = 'smtp.exmail.qq.com'  # 邮件服务器地址
MAIL_PORT = 465               # 邮件服务器端口
MAIL_USERNAME = 'baidu@qq.com' #自己修改
MAIL_PASSWORD = 'uSiPh4ea7z'


LOG_PATH = 'log/phone_web.log'

USER_GROUP_LIST = [1, 2, 3]

CUSTOMER_STATUS_DICT = {'1': 'Active', '2': 'Disable'}

IMPORT_USER_FILE_TYPE_LIST = ['text/csv']


KEY_CHARS = string.ascii_uppercase + string.digits


EMAIL_RE_STRING = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
