import requests
from lxml import html
from datetime import datetime
import pandas as pd
import math

website = "https://www.leboncoin.fr"


def get_all_ads_urls(param_dico, filters_dict):
    i = 1

    result = pd.DataFrame()
    # increment page number while page is not empty
    while True:
        url = website + "/" + param_dico['category'] + "/offres/" + param_dico['region'] + "/"
        filters_dict.update({'o': i})
        page = requests.get(url, params=filters_dict)
        print(page.url)
        tree = html.fromstring(page.content)
        url = tree.xpath('//li[@itemtype="http://schema.org/Offer"]/a/@href')
        date = tree.xpath('//li[@itemtype="http://schema.org/Offer"]/a/section/aside/p/@content')
        if len(url) == 0 or len(date) == 0:
            break
        tmp = pd.DataFrame(data=url, index=date, columns=['url'])
        result = pd.concat([result, tmp])
        i = i + 1
    result['url'] = "http:" + result["url"]
    return result


def min_price_filter(price):
    res = 0
    if price <= 350000:
        res = price / 25000
    elif price > 350000 and price <= 700000:
        res = (price - 350000) / 50000 + 14
    elif price > 700000 and price <= 1500000:
        res = (price - 700000) / 100000 + 21
    elif price > 1500000 and price < 2000000:
        res = 29
    elif price > 2000000:
        res = 30
    return str(int(res))


def max_price_filter(price):
    res = 0.0
    if price > 2000000:
        res = 0.0
    elif price > 700000:
        res = math.ceil(29.0 + price / 100000.0 - 15.0)
    elif price > 350000:
        res = math.ceil(20.0 + price / 50000.0 - 13.0)
    elif price > 0:
        res = math.ceil(13.0 + price / 25000.0 - 13.0)
    return str(int(res))


def max_surface_filter(surface):
    res = 0.0
    if surface > 500:
        res = 0
    elif surface > 300:
        res = 20
    elif surface >= 150:
        res = math.ceil(19.0 + surface / 50.0 - 6.0)
    elif surface >= 40:
        res = math.ceil(15.0 + surface / 10.0 - 14.0)
    elif surface >= 20:
        res = math.ceil(4.0 + surface / 5.0 - 7.0)
    elif surface > 0:
        res = 1
    return str(int(res))


def min_surface_filter(surface):
    res = 0
    if surface < 20:
        res = 0
    elif surface >= 20 and surface <= 40:
        res = (surface - 20) / 5 + 1
    elif surface > 40 and surface <= 150:
        res = (surface - 40) / 10 + 5
    elif surface > 150 and surface < 200:
        res = 16
    elif surface >= 200 and surface < 300:
        res = 17
    elif surface >= 300 and surface < 500:
        res = 18
    elif surface >= 500:
        res = 19
    return str(int(res))


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


def build_filters(param_dico):
    # price min filter
    ps = min_price_filter(param_dico['p_min'])
    # price max filter
    pe = max_price_filter(param_dico['p_max'])
    # surface min filter
    sqs = min_surface_filter(param_dico['s_min'])
    # surface max filter
    sqe = max_surface_filter(param_dico['s_max'])
    # real estate type filter
    ret = immo_type_filter(param_dico['immo_type'])
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
        filter_dico["ret"] = ret
    if param_dico['location'] != "unknown":
        filter_dico["location"] = param_dico['location']
    return filter_dico


def get_ads_info(param_dict):
    filters = build_filters(param_dict)
    urls = get_all_ads_urls(param_dict, filters)
    info = pd.DataFrame(columns=['url', 'description', 'price', 'surface', 'date'])
    # select only urls with date corresponding to date parameter
    for index, row in urls.loc[param_dict['date'].strftime("%Y-%m-%d")].iterrows():
        print(row['url'])
        page = requests.get(row['url'])
        tree = html.fromstring(page.content)
        ad_price = int(tree.xpath('//h2[@class="item_price clearfix"]/@content')[0])
        ad_surface = int(tree.xpath('//div/h2[span = "Surface"]/span[@class="value"]/text()')[0][:-2])
        ad_descriptions = tree.xpath('//div[@class="line properties_description"]/p[@itemprop="description"]/text()')
        ad_description = ''.join(line for line in ad_descriptions)
        ad_date = datetime.strptime(tree.xpath('//p[@class="line line_pro"]/@content')[0], '%Y-%m-%d')
        info.loc[len(info)] = [row['url'], ad_description, ad_price, ad_surface, ad_date]

    # insert price by surface
    info['p_by_meter'] = info['price'] / info['surface']
    info.round({'p_by_meter': 1})
    # filter on price by meter
    info = info[info['p_by_meter'] < param_dict['p_by_meter_max']]
    # filter by surface
    info = info[(info['surface'] > param_dict['s_min']) & (info['surface'] < param_dict['s_max'])]

    return info
