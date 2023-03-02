#
import time
import json

from ..utils.email.mail_gun import MailGun
from ..utils.email.send_pool import EmailSenderPool
from ..utils.email.smtp2go import SMTP2GO
from ..utils.email.sendcloud import SendCloudV2

# test user:
API_USER = "sunnyhong_test_aKHHzD"
API_KEY = "soaUhPv5uqYFEQZh"


def test_send_email():
    mail = {
        "from": "register@btcc.com",
        "to": "yuan.gu@hpe.com",
        # "template_invoke_name": "test_template",
        "fromname": "henry",
        "subject": "BTCC EMAIL Confirm",
        "html": "hello henry. {}".format(time.time()),
    }
    s = SendCloudV2(api_key=API_KEY, api_user=API_USER)

    api_lists = [
        (s.send_email, mail),
    ]

    for func, args in api_lists:
        if args:
            func(args)
        else:
            func()
    return 1


def test_template_list():
    mail = {
        "from": "register@btcc.com",
        "to": "helenagu@@gmail.com",
        # "template_invoke_name": "test_template",

        "fromname": "henry",
        "subject": "主题",
        "html": "hello henry. {}".format(time.time()),
    }

    s = SendCloudV2(api_key=API_KEY, api_user=API_USER)

    api_lists = [
        (s.template_list, None),
    ]

    for func, args in api_lists:
        if args:
            func(args)
        else:
            func()

xsmtpapi = {
        "to": ['604496499@qq.com', ],
        "sub": {
            '%name%': ['Alex Gu', ],
            '%url%': ['123456', ],
        },
    }

# 邮件正文:
email_content = {
    "from": "no_reply@btcc.com",
    "to": '604496499@qq.com',
    "fromName": 'BTCC_Team',
    "subject": '[BTCC] Pass KYC Level 4 Verification',
    # 服务商配置邮件模板ID
    "templateInvokeName": 'kyc_l4',
    "xsmtpapi": json.dumps(xsmtpapi),
}

def test_send_smtp2_email():
    # 注册模板格式:
    s = SMTP2GO()
    r = s.send_template_email(email_content)
    return r


def test_send_mail_gun():
    s = MailGun(api_domain='btc250.com')
    r = s.send_template_email(email_content)
    return r


def test_send_cloud():
    s = SendCloudV2()
    r = s.send_template_email(email_content)
    return r


def test_send_pool():
    template_list = ("btcc_mail", "trade_verify", "kyc_l2", "kyc_l3", "kyc_l4", "kyc_no")
    s = EmailSenderPool()
    for i in template_list:
        email_content.update(templateInvokeName=i)
        s.send_template_sm_mail(email_content)


# coding:utf-8

import requests

import urllib


def test_tem():
    url = "http://api.sendcloud.net/apiv2/mail/sendtemplate"

    xsmtpapi = {
        'to': ['13901849666@139.com', 'test2@ifaxin.com'],
        'sub': {
            '%name%': ['user1', 'user2'],
            '%money%': ['1000', '2000'],
        },
    }

    params = {
        "apiUser": API_USER,  # 使用apiUser和apiKey进行验证
        "apiKey": API_KEY,
        "templateInvokeName": "test12346",
        "xsmtpapi": json.dumps(xsmtpapi),
        "from": "register@btcc.com",
        "fromName": "SendCloud",
        "subject": "BTCC Email Confirmation",
    }

    filename = ".test.html"
    display_filename = "filename"

    #files = { "attachments" : (None, open(filename,"rb"))}

    r = requests.post(url, files=None, data=params)

    print(r.text)
