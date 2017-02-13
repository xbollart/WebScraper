import requests
import HTMLParser
from lxml import html
from datetime import datetime
import math

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

def is_valid(ad,date, price_ratio_max,surface_min, surface_max, keywords):
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

def min_price_filter(price):
    res = 0
    if price <= 350000:
        res = price/25000
    elif price > 350000 and price <= 700000:
        res = (price - 350000)/50000 + 14
    elif price > 700000 and price <= 1500000:
        res = (price - 700000)/100000 + 21
    elif price > 1500000 and price < 2000000:
        res = 29
    elif price > 2000000:
        res = 30
    return str(res)

def max_price_filter(price):
    res = 0
    if price <= 350000:
        res = price/25000 + 1
        if(price%25000 == 0):
            res = res - 1
    elif price > 350000 and price <= 700000:
        res = (price - 350000)/50000 + 15
        if(price%50000 == 0):
            res = res - 1
    elif price > 700000 and price <= 1500000:
        res = (price - 700000)/100000 + 22
        if(price%100000 == 0):
            res = res - 1
    elif price > 1500000:
        res = 30
    return str(res)

def max_surface_filter(surface):
    res = 0
    if surface < 20:
        res = 1
    elif surface >= 20 and surface <= 40:
        res = (surface - 20)/5 + 2
        if(surface%5):
            res = res - 1
    elif surface > 40 and surface <= 150:
        res = (surface - 40)/10 + 6
        if(surface%10):
            res = res - 1
    elif surface > 150 and surface < 200:
        res = 17
    elif surface >= 200 and surface < 300:
        res = 18
    elif surface >= 300 :
        res = 19
    return str(res)

def test_max(surface):
    res = 0.0
    if surface > 500:
        res = 0
    elif surface > 300:
        res = 20
    elif surface >= 150:
        res = math.ceil(19.0 + surface/50.0 - 6.0)
    elif surface >= 40:
        res = math.ceil(15.0 + surface/10.0 - 14.0)
    elif surface >= 20:
        res = math.ceil(4.0 + surface/5.0 -7.0)
    elif surface > 0:
        res = 1
    return str(int(res))

def min_surface_filter(surface):
    res = 0
    if surface < 20:
        res = 0
    elif surface >= 20 and surface <= 40:
        res = (surface - 20)/5 + 1
    elif surface > 40 and surface <= 150:
        res = (surface - 40)/10 + 5
    elif surface > 150 and surface < 200:
        res = 16
    elif surface >= 200 and surface < 300:
        res = 17
    elif surface >= 300 and surface < 500:
        res = 18
    elif surface >= 500 :
        res = 19
    return str(res)

def immo_type_filter(immo_type):
    res = "unknown"
    if immo_type == "maison":
        res = "1"
    elif immo_type == "appartement":
        res = "2"
    elif immo_type == "terrain":
        res = "3"
    elif immo_type == "parking":
        res = "4"
    elif immo_type == "autre":
        res = "5"
    return res


def build_filters(location,p_min, p_max, s_min, s_max, immo_type):
    #price min filter
    ps = min_price_filter(p_min)
    #price max filter
    pe = max_price_filter(p_max)
    #surface min filter
    sqs = surface_filter(s_min)
    #surface max filter
    sqe = surface_filter(s_max)
    # real estate type filter
    ret = immo_type_filter(immo_type)
    filter_dico = {}

    if ps != "0":
        filter_dico["ps"] = ps
    if pe != "0":
        filter_dico["pe"] = pe
    if sqs != "0":
        filter_dico["sqs"] = sqs
    if sqe != "0":
        filter_dico["sqe"] = sqe
    if ret != "none":
        filter_dico["ret"]= ret
    if location != "unknown":
        filter_dico["location"] = location

    return filter_dico

  #  return {'location': 'Rouen 76000','ps':'2','pe':'6','sqs':'1','sqe':'5','ret':'2' }


def get_ads_infos(category, region, location, date, p_min, p_max, s_min, s_max, price_by_meter, immo_type, keywords={}):

    filters = build_filters(location,p_min, p_max, s_min, s_max, immo_type)
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
            ad_description = ad_description + line.encode('utf8')
        ad_date = datetime.strptime(tree.xpath('//p[@class="line line_pro"]/@content')[0], '%Y-%m-%d')
        ad = Advert(url, ad_description, ad_price, ad_surface, ad_date)
        if is_valid(ad, date, price_by_meter, s_min, s_max, keywords):
            infos.append(ad)
    return infos