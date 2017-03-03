from datetime import datetime, timedelta
import utils.leboncoin as leboncoin
import utils.mail as mail


if __name__ == '__main__':
    # set request parameters
    date = datetime.now() - timedelta(days=1)
    date = datetime(date.year, date.month, date.day)
    to = "xavier.bollart@gmail.com"
    param_dict = {}
    param_dict['category'] = 'ventes_immobilieres'
    param_dict['region'] = 'haute_normandie'
    param_dict['location'] = 'Rouen 76000'
    param_dict['immo_type'] = 'appartement'
    param_dict['date'] = date
    param_dict['p_max'] = 120000
    param_dict['p_min'] = 50000
    param_dict['s_min'] = 20
    param_dict['s_max'] = 40
    param_dict['p_by_meter_max'] = 3000

    ads_details = leboncoin.get_ads_info(param_dict)
    
    # send Mail
    body = mail.build_body(ads_details)
    if len(body) > 0:
        mail.send_mail(to, "Rouen Daily Report", body)