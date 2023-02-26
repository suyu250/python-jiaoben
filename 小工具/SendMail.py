import smtplib
from email.mime.text import MIMEText


def send_email(text, subject):
    message = MIMEText(text, 'plain', 'utf-8')
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = receivers[1]
    try:
        stmpobj = smtplib.SMTP()
        stmpobj.connect(mail_host, 25)
        stmpobj.login(mail_user, mail_pass)
        stmpobj.sendmail(sender, receivers, message.as_string())
        stmpobj.quit()
        return True
    except smtplib.SMTPException:
        return False


mail_host = 'smtp.qq.com'
mail_user = ''
mail_pass = ''

sender = ''
receivers = ['']

print(send_email(text='测试', subject='主题测试'))
