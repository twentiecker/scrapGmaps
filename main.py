import scraping

url = "https://www.google.co.id/maps/place/Bogor+Cafe/@-6.172172,106.8266993,15z/data=!4m9!1m2!2m1!1srestaurant+or+cafe!3m5!1s0x2e69f5cc0abf0f67:0x78dce6deb9815e6!8m2!3d-6.172172!4d106.835454!15sChJyZXN0YXVyYW50IG9yIGNhZmVaFCIScmVzdGF1cmFudCBvciBjYWZlkgEVaW5kb25lc2lhbl9yZXN0YXVyYW50mgEkQ2hkRFNVaE5NRzluUzBWSlEwRm5TVVI1TFdWUFVISlJSUkFC"
scrap = scraping.Scraping()
data = scrap.scrape(url)
print(data)
print(data['title'])
