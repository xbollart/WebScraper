import requests

website = "https://www.leboncoin.fr"
category = "ventes_immobilieres"
region = "haute_normandie"
#ps = prix min 0 = aucun
filters = {'o': '1','location': 'Rouen 76000','ps':'2','pe':'6','sqs':'1','sqe':'5','ret':'2' }
url = website + "/" + category + "/offres/" + region + "/"
r = requests.get(url, params=filters)
print(r.url)

