import requests

website = "https://www.leboncoin.fr"
category = "ventes_immobilieres"
region = "haute_normandie"
filters = "ps=2&pe=6&sqs=1&sqe=5&ret=2"
page_filter = "o=1"

url = website + "/" + category + "/offres/" + region + "/"
payload = {'o': '1','location': 'Rouen 76000','ps':'2','pe':'6','sqs':'1','sqe':'5','ret':'2' }
r = requests.get(url, params=payload)
print(r.url)

