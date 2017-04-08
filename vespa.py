from datetime import datetime, timedelta
import utils.leboncoin as leboncoin
import utils.mail as mail

if __name__ == '__main__':
    # set request parameters
    date = datetime.now() - timedelta(days=1)
    date = datetime(date.year, date.month, date.day)
    to = "xavier.bollart@gmail.com"
    param_dict = {}
    param_dict['category'] = 'motos'
    param_dict['region'] = 'ile_de_france'

    param_dict['date'] = date
    param_dict['p_max'] = 60000
    param_dict['p_min'] = 0
    param_dict['s_min'] = 0
    param_dict['s_max'] = 25

    ads_details = leboncoin.get_ads_info(param_dict)

    # send Mail
    body = mail.build_body(ads_details)
    if len(body) > 0:
        mail.send_mail(to, "parking paris Daily Report", body)