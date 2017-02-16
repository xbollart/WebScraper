
import utils.leboncoin
from datetime import datetime, timedelta

# website = "https://www.leboncoin.fr"
# category = "ventes_immobilieres"
# region = "haute_normandie"
# #ps = prix min 0 = aucun
# filters = {'o': '1','location': 'Rouen 76000','ps':'2','pe':'6','sqs':'1','sqe':'5','ret':'2' }
# url = website + "/" + category + "/offres/" + region + "/"
# r = requests.get(url, params=filters)
# print(r.url)

date = datetime.now() - timedelta(days=1)
date_min = datetime(date.year, date.month, date.day)
date_max = datetime.now()

print date_min
print date_max







