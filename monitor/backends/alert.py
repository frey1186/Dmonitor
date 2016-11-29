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


class AlarmProcessor(object):
    def __init__(self,models,MQ_CONN_OBJ):
        self.models = models
        self.mq_conn_obj = MQ_CONN_OBJ
        pass

    def get_alarm_list(self):
        pass

    def alarm_or_not(self):
        pass

    def alarm_content_edit(self):
        pass


    def send_alarm_to_mq(self):
        pass


class AlarmStart(object):
    def __init__(self, MQ_CONN_OBJ):
        self.mq_conn_obj = MQ_CONN_OBJ

    def get_alarm_from_mq(self):
        pass
    def send_email(self,email_to,email_subject,email_text,email_from):
        pass







if __name__ == "__main__":
    SendEmail("yangfeilong_2009@126.com", "hello2", "hello world  22222")