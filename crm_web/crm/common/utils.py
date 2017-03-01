# -*- coding: utf-8 -*-

import os
import re
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
from IPython import embed
import jwt
from time import time

from crm import settings

import sys
reload(sys)
sys.setdefaultencoding('utf8')



def strip_lower(data):
    """对传入的字符串进行strip和lower操作并去掉空格
    """
    return data.lower().strip().replace(' ','')


def csv2list(data):
    """将csv文件内容转换为list返回
    """
    result = []
    lines = data.splitlines()[1:]
    for i in lines:
        result.append(i.split(','))
    return result


class phoneSendEmail(object):
    '''发送邮件
    '''

    def __init__(cls,mail_subject):
        cls.from_addr = settings.MAIL_USERNAME
        cls.mail_account = settings.MAIL_USERNAME
        cls.mail_password = settings.MAIL_PASSWORD
        cls.mail_subject = mail_subject
        cls.smtp_server = settings.MAIL_SERVER
        cls.smtp_port = settings.MAIL_PORT

    def _format_addr(cls, s):
        """格式化地址
        """
        name, addr = parseaddr(s)
        return formataddr(( \
            Header(name, 'utf-8').encode(), \
            addr.encode('utf-8') if isinstance(addr, unicode) else addr))


    def send(cls, msg_content, to_addr):
        """发送邮件
        """
        _format_addr = cls._format_addr
        from_addr = cls.from_addr
        mail_subject  = cls.mail_subject
        smtp_port = cls.smtp_port
        smtp_server = cls.smtp_server
        mail_account = cls.mail_account
        mail_password = cls.mail_password

        msg = MIMEText(msg_content, 'html', 'utf-8')
        msg['From'] = _format_addr(u'CRM <{}>'.format(from_addr))
        msg['To'] = _format_addr(to_addr)
        msg['Subject'] = _format_addr(mail_subject)

        server = smtplib.SMTP_SSL(smtp_server, smtp_port)

        server.login(mail_account, mail_password)
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()



def custom_secure_filename(filename):
    """ 将不安全的文件名转换为安全的可以在文件系统实用的安全文件名
    """
    filename = filename.encode('utf-8')

    for sep in os.path.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, ' ')

    # unicode 中文编码范围为 /u4e00-/u9fa5
    _filename_zh_ascii_strip_re = re.compile(u"[^A-Za-z0-9_.-\u4e00-\u9fa5]")
    _windows_device_files = ('CON', 'AUX', 'COM1', 'COM2', 'COM3', 'COM4', 'LPT1',
                             'LPT2', 'LPT3', 'PRN', 'NUL')

    filename = str(_filename_zh_ascii_strip_re.sub('', '_'.join(filename.split()))).strip('._')

    if os.name == 'nt' and filename and filename.split('.')[0].upper() in _windows_device_files:
        filename = '_' + filename

    return filename
