import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def send_simple_mail(TO, SUBJECT, TEXT):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("snoopy.bollart@gmail.com", "YJZ-4DA-zDd-T8H")
    
    msg = "my message"
    server.sendmail("xavier.bollart@gmail.com", "xavier.bollart@gmail.com", msg)
    server.quit()


def build_body(ads):
    body = ""
    i = 1
    for index, row in ads.iterrows():
        body = body + "appartement no " + str(i) + ":  " + str(row['surface']) + " m2    " + str(row['p_by_meter']) + " euro/m2" + os.linesep
        body = body + row['url'] + os.linesep + os.linesep
        i = i + 1
    return body


def send_mail( m_to, m_subject, m_body, m_file_path = "", m_file_name = ""):
    m_from = "snoopy.bollart@gmail.com"
    m_pwd = "YJZ-4DA-zDd-T8H"

    msg = MIMEMultipart()

    msg['From'] = m_from
    msg['To'] = m_to
    msg['Subject'] = m_subject

    msg.attach(MIMEText(m_body, 'plain'))

    if m_file_path != "":
        attachment = open(m_file_path, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % m_file_name)
        msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(m_from, m_pwd)
    text = msg.as_string()
    server.sendmail(m_from, m_to, text)
    server.quit()