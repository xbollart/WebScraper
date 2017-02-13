
import utils.leboncoin

# website = "https://www.leboncoin.fr"
# category = "ventes_immobilieres"
# region = "haute_normandie"
# #ps = prix min 0 = aucun
# filters = {'o': '1','location': 'Rouen 76000','ps':'2','pe':'6','sqs':'1','sqe':'5','ret':'2' }
# url = website + "/" + category + "/offres/" + region + "/"
# r = requests.get(url, params=filters)
# print(r.url)

print(utils.leboncoin.max_price_filter(10000))
print(utils.leboncoin.max_price_filter(25000))
print(utils.leboncoin.max_price_filter(40000))
print(utils.leboncoin.max_price_filter(50000))
print(utils.leboncoin.max_price_filter(340000))
print(utils.leboncoin.max_price_filter(350000))
print(utils.leboncoin.max_price_filter(360000))
print(utils.leboncoin.max_price_filter(400000))
print(utils.leboncoin.max_price_filter(660000))
print(utils.leboncoin.max_price_filter(700000))

