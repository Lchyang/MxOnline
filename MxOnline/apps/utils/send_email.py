from random import randint

from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from MxOnline.settings import EMAIL_FROM


# 生成一个随机字符串
def random_str(random_len=8):
    _str = ''
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    length = len(chars) - 1
    for i in range(random_len):
        _str += chars[randint(0, length)]
    return _str


def send_register_email(email, send_type='register'):
    code = random_str(16)  # 生成随机字符串
    email_record = EmailVerifyRecord()
    email_record.code = code   # 将随机字符串、邮箱、发送类型、保存到同一个表中，在emailverifyrecord(),和user_profile()
    email_record.email = email   # 都存在同一个邮箱可以通过邮箱进行两个表的交互。
    email_record.send_type = send_type
    email_record.save()
    if send_type == 'register':
        # 设置邮件发送的内容
        email_title = '在线教育网注册激活链接'
        email_body = '请点击下面的链接激活您的账号 http://127.0.0.1:8000/active/{}'.format(code)
        # 通过send_mail函数发送邮件返回一个布尔值
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    if send_type == 'forget':
        # 设置邮件发送的内容
        email_title = '在线教育网注册重置密码链接'
        email_body = '请点击下面的链接重置您的密码 http://127.0.0.1:8000/revert/{}'.format(code)
        # 通过send_mail函数发送邮件返回一个布尔值
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

