import os
from datetime import datetime, timedelta
import utils.leboncoin
import utils.mail

def build_body(ads):
    body = ""
    for i in range(0, len(ads)):
        ad = ads[i]
        body = body + "appartement no " + str(i+1) +":  "+ str(ad.surface) + " m2    " + str(ad.price_by_meter()) +" euro/m2" + ad.remark + os.linesep
        body = body + ad.url + os.linesep + os.linesep
    return body

if __name__ == '__main__':

    date = datetime.now() #- timedelta(days=1)
    price_by_meter_max = 5000
    surface_min = 20
    surface_max = 40
    price_min = 50000
    price_max =300000
    keywords = ["Dock","cauchoise","beauvoisine"]
    category = "ventes_immobilieres"
    region = "aquitaine"
    location = "Bordeaux 33000"
    immo_type = "appartement"
    to = "xavier.bollart@gmail.com"
    date = datetime(date.year, date.month, date.day)
    ads_details = utils.leboncoin.get_ads_infos(category, region, location, date, price_min, price_max, surface_min, surface_max, price_by_meter_max, immo_type, keywords)
    body = build_body(ads_details)
    if(len(body) > 0):
        utils.mail.send_mail(to,"Bordeaux Daily Report",body)