from datetime import datetime, timedelta
import utils.leboncoin as leboncoin
import utils.mail as mail


if __name__ == '__main__':
    # set request parameters
    date = datetime.now()
    date = date - timedelta(days=1)
    p_max_by_m2 = 3000
    s_min = 20
    s_max = 40
    p_min = 50000
    p_max =120000
    category = "ventes_immobilieres"
    region = "haute_normandie"
    location = "Rouen 76000"
    immo_type = "appartement"
    to = "xavier.bollart@gmail.com"
    date = datetime(date.year, date.month, date.day)
    ads_details = leboncoin.get_ads_info(category, region, location, date, p_min, p_max, s_min, s_max, p_max_by_m2, immo_type)

    # send Mail
    body = mail.build_body(ads_details)
    if len(body) > 0:
        mail.send_mail(to, "Rouen Daily Report", body)