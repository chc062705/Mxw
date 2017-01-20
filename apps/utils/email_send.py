# -*- coding:utf-8 -*-
from users.models import EmailVerifyRecord
from random import Random
from django.core.mail import send_mail
from untitled.settings import EMAIL_FROM
def random_str(randomlength=8):
    str=""
    chars='AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz01234567890'
    length=len(chars)-1
    random=Random()
    for i in range(randomlength):
        str+=chars[random.randint(0,length)]
    return str

def send_register_email(email,semd_type="register"):
    email_record=EmailVerifyRecord()
    if semd_type=="update":
        code=random_str(4)
    else:
        code=random_str(16)
    email_record.code=code
    email_record.email=email
    email_record.send_type=semd_type
    email_record.save()
    email_tittle=""
    email_body=""
    if semd_type=="register":
        email_tittle="激活账户"
        email_body="请你电机链接：http:/127.0.0.1:8000/active/{0}".format(code)
        send_status=send_mail(email_tittle,email_body,EMAIL_FROM,[email])
        if send_status:
            pass
    elif semd_type=="forget":
        email_tittle="忘记密码"
        email_body="请你电机链接：http:/127.0.0.1:8000/active/{0}".format(code)
        send_status=send_mail(email_tittle,email_body,EMAIL_FROM,[email])
        if send_status:
            pass
    elif semd_type=="update":
        email_tittle="修改邮箱账号"
        email_body="邮箱验证码：{0}".format(code)
        send_status=send_mail(email_tittle,email_body,EMAIL_FROM,[email])
        if send_status:
            pass