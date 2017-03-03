
from datetime import datetime, timedelta
import utils.leboncoin
import utils.file

if __name__ == '__main__':

    date = datetime(2017, 1, 30)
    date = datetime.now()
    price_by_meter_max = 3000
    surface_min = 20
    surface_max = 40
    price_min = 50000
    price_max =120000
    keywords = ["Dock","cauchoise","beauvoisine"]
    category = "ventes_immobilieres"
    region = "haute_normandie"
    location = "Rouen 76000"
    immo_type = "appartement"
    to = "xavier.bollart@gmail.com"
    file_name = "output.csv"

    ads_details = utils.leboncoin.get_ads_info(category, region, location, date, price_min, price_max, surface_min, surface_max, price_by_meter_max, immo_type, keywords)

    ads_arr = [[ad.date.strftime("%Y-%m-%d %H:%M"),str(ad.price),str(ad.surface),ad.description] for ad in ads_details]

    utils.file.write_csv_file(ads_arr,file_name)