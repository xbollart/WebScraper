from datetime import datetime, timedelta
import utils.leboncoin as leboncoin
import utils.mail as mail


if __name__ == '__main__':
    # set request parameters
    date = datetime.now()
    date = date - timedelta(days=1)
    date = datetime(date.year, date.month, date.day)
    p_max_by_m2 = 0
    s_min = 0
    s_max = 0
    p_min = 0
    p_max =60000
 #   category = "ventes_immobilieres"
 #   region = "ile_de_france"
  #  location = "Paris"
 #   immo_type = "parking"
    to = "xavier.bollart@gmail.com"

    param_dict = {}
    param_dict['category'] = 'ventes_immobilieres'
    param_dict['region'] = 'ile_de_france'
    param_dict['location'] = 'Paris'
    param_dict['immo_type'] = 'parking'
  #  param_dict['to'] = 'xavier.bollart@gmail.com'




    ads_details = leboncoin.get_ads_info(param_dict, date, p_min, p_max, s_min, s_max, p_max_by_m2)
    
    # send Mail
    body = mail.build_body(ads_details)
    if len(body) > 0:
        mail.send_mail(to, "parking paris Daily Report", body)