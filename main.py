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

url = "https://www.google.co.id/maps/search/restaurant+or+cafe/@-6.1721719,106.8266993,15z/data=!3m1!4b1"

# Set options for driver
opts = Options()
opts.add_argument("--headless")
opts.add_argument("--no-sandbox")
opts.add_argument("--window-size=1420,1080")
opts.add_argument("--disable-gpu")
opts.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36")

# Initiate selenium driver
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=opts)
driver.get(url)

# Initiating module
navigate = navigating.Navigating(driver, url)

# Check prerequisite home page
navigate.prerequisite_home()

time.sleep(5)

# Scroll home page to bottom
navigate.scroll_home()
print(f"max_count = {navigate.max_count}")

i = 0
while (i < navigate.max_count):
    print("======================================")
    print(f"============= Scrap ke-{i + 1} =============")
    print("======================================")

    # Click item one by one in home page
    time.sleep(5)
    navigate.click_items_home(i)

    # Check prerequisite detail page
    time.sleep(5)
    navigate.prerequisite_detail()

    # Continue the loop if nothing "popular times" in detail page
    try:
        WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.CLASS_NAME, 'g2BVhd')))
    except TimeoutException:
        # Scroll home page to bottom
        navigate.scroll_home()
        print(f"max_count = {navigate.max_count}")

        i = i + 1
        continue

    scrap = scraping.Scraping(driver)
    # data = scrap.scrape(url)
    data = scrap.scrape()
    print(data)
    # print(data['title'])

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

    # Scroll home page to bottom
    navigate.scroll_home()
    print(f"max_count = {navigate.max_count}")

# Next page
WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.CLASS_NAME, "hV1iCc")))
page = driver.find_elements(By.CLASS_NAME, "hV1iCc")
for i in page:
    j = i.get_attribute("jsaction")
    if j == "pane.paginationSection.nextPage":
        i.click()
        break
print("*** Next page ***")
time.sleep(5)
