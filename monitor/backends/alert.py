#_*_coding:utf-8_*_
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def SendEmail(toAdd, subject, htmlText, attachfile='', fromAdd='yangfeilong_2009@126.com'):
    strFrom = fromAdd
    strTo = toAdd
    msg = MIMEText(htmlText)
    msg['Content-Type'] = 'Text/HTML'
    msg['Subject'] = Header(subject, 'utf-8')
    msg['To'] = strTo
    msg['From'] = strFrom

    smtp = smtplib.SMTP('smtp.126.com')
    smtp.login('yangfeilong_2009@126.com', 'fy123!@#')
    try:
        smtp.sendmail(strFrom, strTo, msg.as_string())
        print 'Send email successful.'
    finally:
        smtp.close()


if __name__ == "__main__":
    SendEmail("yangfeilong_2009@126.com", "hello2", "hello world  22222")