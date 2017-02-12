import os
from lxml import html
from datetime import datetime, timedelta
import utils.leboncoin
import utils.mail

def build_body(ads):
    body = ""
    for i in range(0, len(ads)):
        ad = ads[i]
        body = body + "appartement no " + str(i+1) +":  "+ str(ad.surface) + " m2    " + str(ad.price_by_meter()) +" euro/m2"+ ad.remark + os.linesep
        body = body + ad.url + os.linesep + os.linesep
    return body

if __name__ == '__main__':

    print ("Start scraping Rouen Appartements")
    date = datetime.now() - timedelta(days=1)
    price_by_meter_max = 3000
    surface_min = 25
    surface_max = 40
    keywords = ["Dock","cauchoise","beauvoisine"]
    category = "ventes_immobilieres"
    region = "haute_normandie"
    filters = {'location': 'Rouen 76000','ps':'2','pe':'6','sqs':'1','sqe':'5','ret':'2' }
    to = "xavier.bollart@gmail.com"
    date = datetime(date.year, date.month, date.day)
    print ("Date of research: " + str(date))
    ads_details = utils.leboncoin.get_ads_infos(category, region, filters, date, price_by_meter_max, surface_min, surface_max, keywords)
    print ("Nb of ads matching criteria: " + str(len(ads_details)))
    print("Send report to: " + to)
    body = build_body(ads_details)
    if(len(body) > 0):
        utils.mail.send_mail(to,"Rouen Daily Report",body)