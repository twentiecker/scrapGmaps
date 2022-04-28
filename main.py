from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time
import scraping
import navigating

# Navigating
url = "https://www.google.co.id/maps/search/restaurant+or+cafe/@-6.1721719,106.8266993,15z/data=!3m1!4b1"

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get(url)

# Initiating process
navigate = navigating.Navigating(driver)

# Check prerequisite home page
navigate.prerequisite_home()

i = 0
while (i < 1):
    # Click item one by one in home page
    time.sleep(5)
    navigate.click_items_home(i)

    # Check prerequisite detail page
    time.sleep(5)
    navigate.prerequisite_detail(i)

    # Scraping
    # url = "https://www.google.co.id/maps/place/Bogor+Cafe/@-6.172172,106.8266993,15z/data=!4m9!1m2!2m1!1srestaurant+or+cafe!3m5!1s0x2e69f5cc0abf0f67:0x78dce6deb9815e6!8m2!3d-6.172172!4d106.835454!15sChJyZXN0YXVyYW50IG9yIGNhZmVaFCIScmVzdGF1cmFudCBvciBjYWZlkgEVaW5kb25lc2lhbl9yZXN0YXVyYW50mgEkQ2hkRFNVaE5NRzluUzBWSlEwRm5TVVI1TFdWUFVISlJSUkFC"
    scrap = scraping.Scraping(driver)
    # data = scrap.scrape(url)
    data = scrap.scrape()
    print(data)
    print(data['title'])

    # Back to detail page from review page
    navigate.back_to_detail()
    time.sleep(5)

    # Back to home page from review page
    back_home = driver.find_element(By.CLASS_NAME, 'hYBOP')
    img_back_home = back_home.find_element(By.TAG_NAME, 'img')
    img_validate = img_back_home.get_attribute('src')
    if img_validate == "https://www.gstatic.com/images/icons/material/system_gm/1x/arrow_back_black_24dp.png":
        navigate.back_to_home()
        time.sleep(5)

    i = i + 1

# Next page
page = driver.find_elements(By.CLASS_NAME, "hV1iCc")
for i in page:
    j = i.get_attribute("jsaction")
    if j == "pane.paginationSection.nextPage":
        i.click()
        break
print("next page")
time.sleep(5)
