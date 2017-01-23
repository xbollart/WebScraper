import requests
import os
from lxml import html
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def build_url(page_nb):
    website = "https://www.leboncoin.fr/ventes_immobilieres/offres"
    region = "haute_normandie"
    departement = "seine_maritime"
    page_filter = "o="+ str(page_nb)
    filters = "ps=2&pe=6&sqs=1&sqe=5&ret=2&location=Rouen%2076000"

    return website + "/" + region + "/" +departement + "/?" +page_filter +"&"+ filters

def get_all_ads_urls():
    i = 1
    links = []

    while True:
        url = build_url(i)
        i = i+1
        page = requests.get(url)
        tree = html.fromstring(page.content)
        res = [ "http:" + link for link in tree.xpath('//a[@class="list_item clearfix trackable"]/@href')]
        if len(res) == 0:
            break
        links = links + res
    return links

def write_text_file(ads,file_name):
    stream = open(file_name, "w")
    for ad in ads:
        stream.write(" price: " + str(ad[1]) + " surface: " + str(ad[2]) + os.linesep)
        stream.write(ad[0] + os.linesep)
    stream.close()

def write_csv_file(ads,file_name):
    stream = open(file_name, "w")
    stream.write("surface,price,prix/m2,url" + os.linesep)
    for ad in ads:
        stream.write(str(ad[2]) + "," + str(ad[1]) + "," + str(ad[1]/ad[2]) + "," + ad[0] + os.linesep)
    stream.close() 

def is_valid(ad,date, price_ratio_max,surface_min, surface_max):
    is_valid = True
    # Check date is yesterday
    if ad[4] != date:
        is_valid = False
        print("Date invalid")
    # # Check price per square meter
    if ad[1]/ad[2] > price_ratio_max:
        is_valid = False
        print("price too high")
    # # Check surface
    if ad[2]< surface_min or ad[2] > surface_max:
        is_valid = False
        print("surface not matching")

    return is_valid

def get_ads_infos(urls,date,price,s_min,s_max):
    infos = []
    for url in urls:
        print(url)
        page = requests.get(url)
        tree = html.fromstring(page.content)
        ad_price = int(tree.xpath('//h2[@class="item_price clearfix"]/@content')[0])
        ad_surface = int(tree.xpath('//div/h2[span = "Surface"]/span[@class="value"]/text()')[0][:-2])
        ad_description = tree.xpath('//div[@class="line properties_description"]/p[@itemprop="description"]/text()')
        ad_date = datetime.strptime(tree.xpath('//p[@class="line line_pro"]/@content')[0], '%Y-%m-%d')
        ad = [url,ad_price,ad_surface,ad_description,ad_date]
        if is_valid(ad,date,price,s_min,s_max):
            infos.append(ad)
    return infos

def send_simple_mail(TO,SUBJECT,TEXT):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("xavier.bollart@gmail.com", "Geekgm02")
    msg = "my message"
    server.sendmail("xavier.bollart@gmail.com", "xavier.bollart@gmail.com", msg)
    server.quit()

def send_mail( m_to, m_subject, m_body,m_file_path = "",m_file_name = ""):
    m_from = "xavier.bollart@gmail.com"
    m_pwd = "Geekgm02"

    msg = MIMEMultipart()

    msg['From'] = m_from
    msg['To'] = m_to
    msg['Subject'] = m_subject

    msg.attach(MIMEText(m_body, 'plain'))

    if (m_file_path != ""):
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

def build_body(ads):
    body = ""
    for i in range(0, len(ads)):
        ad = ads[i]
        body = body + "appartement no " + str(i+1) +":  "+ str(ad[2]) + " m2    " + str(ad[1]/ad[2]) +" euro/m2"+ os.linesep
        body = body + ad[0] + os.linesep + os.linesep   
    return body

print("Start scraping leboncoin.fr")
date = datetime.now()
price = 3000
surface_min = 25
surface_max = 40
to = "xavier.bollart@gmail.com"
previous_day = datetime(date.year, date.month, date.day-1)
print("Date of research: " + str(previous_day))
ads_urls = get_all_ads_urls()
print("Nb of ads found: " + str(len(ads_urls)))
ads_details = get_ads_infos(ads_urls,previous_day,price,surface_min,surface_max)
print("Nb of ads matching criteria: " + str(len(ads_details)))
file_name = previous_day.strftime('%d-%m-%Y') +"_leboncoin.csv"
#print("Generate CSV file: " + file_name)
#write_csv_file(ads_details,file_name)
print("Send report to: " + to)
body = build_body(ads_details)
send_mail(to,"Rouen Daily Report",body)