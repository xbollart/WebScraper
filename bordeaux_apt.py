from datetime import datetime, timedelta
import utils.leboncoin as leboncoin
import utils.mail as mail

if __name__ == '__main__':
    # set request parameters
    date = datetime.now() - timedelta(days=1)
    date = datetime(date.year, date.month, date.day)
    p_max_by_m2 = 5000
    s_min = 20
    s_max = 40
    p_min = 50000
    p_max = 300000

    to = "xavier.bollart@gmail.com"

    param_dict = {}
    param_dict['category'] = 'ventes_immobilieres'
    param_dict['region'] = 'haute_normandie'
    param_dict['location'] = 'Rouen 76000'
    param_dict['immo_type'] = 'appartement'


    ads_details = leboncoin.get_ads_info(param_dict, date, p_min, p_max, s_min, s_max, p_max_by_m2)

    # send Mail
    body = mail.build_body(ads_details)
    if len(body) > 0:
        mail.send_mail(to, "Bordeaux Daily Report", body)