import os
from lxml import html
from datetime import datetime, timedelta
import utils.leboncoin
import utils.file


if __name__ == '__main__':

    date = datetime(2017, 1, 30)
    price_by_meter_max = 3000
    surface_min = 25
    surface_max = 40
    category = "ventes_immobilieres"
    region = "haute_normandie"
    filters = {'location': 'Rouen 76000','ps':'2','pe':'6','sqs':'1','sqe':'5','ret':'2' }
    file_name = "rouen_30012017.csv"

    ads_details = utils.leboncoin.get_ads_infos(category, region, filters, date, price_by_meter_max, surface_min, surface_max)

    ads_arr = [[ad.date.strftime("%Y-%m-%d %H:%M"),str(ad.price),str(ad.surface),ad.description] for ad in ads_details]

    utils.file.write_csv_file(ads_arr,file_name)