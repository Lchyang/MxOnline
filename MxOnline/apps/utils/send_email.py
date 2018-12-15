from random import randint

from django.core.mail import send_mail

from users.models import EmailVerifyRecord


# 生成一个随机字符串
def random_str(random_len=8):
    _str = ''
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    length = len(chars) - 1
    for i in range(random_len):
        _str += chars[randint(0, length)]
    return _str


def send_register_email(email, send_type='register'):
    code = random_str(16)
    email_record = EmailVerifyRecord()
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    if send_type == 'register':
        email_title = '在线教育网注册激活链接'
        email_body = '请点击下面的链接激活您的账号 http'