import requests
from lxml import html
from datetime import datetime

website = "https://www.leboncoin.fr"

class Advert():
    def __init__(self, url, description, price, surface, date):
        self.url = url
        self.description = description
        self.price = price
        self.surface = surface
        self.date = date
        self.remark = ""
        

    def price_by_meter(self):
        return self.price/self.surface

def get_all_ads_urls(category, region, filters_dict):
    i = 1
    links = []
    #increment page number while page is not empty
    while True:
        url = website + "/" + category + "/offres/" + region + "/"
        filters_dict.update({'o': i})
        page = requests.get(url, params=filters_dict)
        print(page.url)
        tree = html.fromstring(page.content)
        res = [ "http:" + link for link in tree.xpath('//a[@class="list_item clearfix trackable"]/@href')]
        if len(res) == 0:
            break
        links = links + res
        i = i+1
    return links

def is_valid(ad,date, price_ratio_max,surface_min, surface_max,keywords):
    is_valid = True
    # Check date is yesterday
    if ad.date != date:
        is_valid = False
        print ("Date invalid") 
    # Check price per square meter
    print (ad.price_by_meter())
    if ad.price_by_meter() > price_ratio_max:
        is_valid = False
        print ("price too high")
    # Check surface
    if ad.surface < surface_min or ad.surface > surface_max:
        is_valid = False
        print ("surface not matching")
    # Check Keywords
    for keyword in keywords:
        if keyword in ad.description:
            ad.remark = ad.remark + " #"+keyword
    return is_valid

def get_ads_infos(category, region, filters,date,price,s_min,s_max,keywords={}):

    urls = get_all_ads_urls(category, region, filters)

    infos = []
    for url in urls:
        print(url)
        page = requests.get(url)
        tree = html.fromstring(page.content)
        ad_price = int(tree.xpath('//h2[@class="item_price clearfix"]/@content')[0])
        ad_surface = int(tree.xpath('//div/h2[span = "Surface"]/span[@class="value"]/text()')[0][:-2])
        ad_descriptions = tree.xpath('//div[@class="line properties_description"]/p[@itemprop="description"]/text()')
        ad_description = ""
        for line in ad_descriptions:
            ad_description = ad_description + line
        ad_date = datetime.strptime(tree.xpath('//p[@class="line line_pro"]/@content')[0], '%Y-%m-%d')
        ad = Advert(url, ad_description, ad_price, ad_surface, ad_date)
        if is_valid(ad, date, price, s_min, s_max, keywords):
            infos.append(ad)
    return infos