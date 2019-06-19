import smtplib
from email.mime.text import MIMEText

from data import data


def send_email(text):
    id = data.get('id')
    password = data.get('password')
    email = f'{id}@gmail.com'

    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp.login(id, password)
    print("Login Success")

    msg = MIMEText(text, "html")
    msg['Subject'] = '오늘의 채용 공고'
    msg['To'] = email
    smtp.sendmail(email, email, msg.as_string())
    print("Successfully send email")
    smtp.quit()

