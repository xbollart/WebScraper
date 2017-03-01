
import requests
from lxml import html
from datetime import datetime, timedelta
import math
import pandas as pd 
from pandas import DataFrame, read_csv


# print stream
url = 'https://www.leboncoin.fr/ventes_immobilieres/offres/ile_de_france/?th=1&location=Paris&parrot=0'
page = requests.get(url)
tree = html.fromstring(page.content)

url = tree.xpath('//li[@itemtype="http://schema.org/Offer"]/a/@href')
date = tree.xpath('//li[@itemtype="http://schema.org/Offer"]/a/section/aside/p/@content')

df = pd.DataFrame(data = list(zip(url,date)), columns=['urls', 'dates'])
df.to_csv('../res.csv',index=False,header=False)




