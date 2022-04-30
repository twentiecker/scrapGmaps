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
import writing

# Set an URL
url = "https://www.google.co.id/maps/search/restaurant+or+cafe/@-6.1721719,106.8266993,15z/data=!3m1!4b1"

# Set options for driver
opts = Options()
opts.add_argument("--headless")
opts.add_argument("--no-sandbox")
opts.add_argument("--window-size=1420,1080")
opts.add_argument("--disable-gpu")
opts.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36")

# Initiating selenium driver
service = ChromeService(executable_path=ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service, options=opts)
driver = webdriver.Chrome(service=service)
driver.get(url)

# Initiating module
navigate = navigating.Navigating(driver, url)
write = writing.Writing()
scrap = scraping.Scraping(driver)

time.sleep(5)
# Check prerequisite home page
navigate.prerequisite_home()

print("======================================")

time.sleep(3)
# Scroll home page to bottom
navigate.scroll_home()
print(f"*** all items has been loaded (loaded items: {navigate.max_count})")

i = 0
while i < navigate.max_count:
    print("======================================")
    print(f"*** Scrap {i + 1} ***")

    # Click item one by one after scrolling home page
    time.sleep(3)
    navigate.click_items_home(i)

    # Check prerequisite detail page
    time.sleep(5)
    navigate.prerequisite_detail()

    time.sleep(5)
    # Continue the loop if nothing "popular times" in detail page
    try:
        WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.CLASS_NAME, 'g2BVhd')))
    except TimeoutException:
        # Scroll home page to bottom
        navigate.scroll_home()
        i = i + 1
        continue

    data = scrap.scrape()
    print(data)
    # print(data['title'])
    time.sleep(1)

    # Back to detail page from review page
    navigate.back_to_detail()
    time.sleep(3)

    # Back to home page from detail page
    navigate.back_to_home()
    time.sleep(3)

    i = i + 1

    # Scroll home page to bottom
    navigate.scroll_home()

# Next page
WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.CLASS_NAME, "hV1iCc")))
page = driver.find_elements(By.CLASS_NAME, "hV1iCc")
for i in page:
    j = i.get_attribute("jsaction")
    if j == "pane.paginationSection.nextPage":
        ActionChains(driver).move_to_element(i).perform()
        time.sleep(1)
        ActionChains(driver).move_to_element(i).click(i).perform()
        print("======================================")
        print("*** Next page ***")
        time.sleep(5)
        break

# Case if the display of gmaps website not in common form
# while True:
#     try:
#         # Get is a method that will tell the driver to open at that particular URL
#         # self.driver.get(url)
#
#         if (WebDriverWait(self.driver, 20).until(
#                 ec.presence_of_element_located((By.CLASS_NAME, 'xoLGzf-icon')))):
#             burger_menu = self.driver.find_element(By.CLASS_NAME, 'xoLGzf-icon')
#             if burger_menu.get_attribute(
#                     'src') == "https://www.gstatic.com/images/icons/material/system_gm/1x/menu_black_24dp.png":
#                 print("Oops, sorry wrong website!")
#                 print("===========================================")
#                 print("Attempting to get a right website!")
#                 self.driver.quit()
#                 self.driver = webdriver.Chrome(service=self.service)
#                 continue
#             else:
#                 # Waiting for the page to load element "popular times"
#                 WebDriverWait(self.driver, 20).until(
#                     ec.presence_of_element_located((By.CLASS_NAME, 'g2BVhd')))
#
#                 print("Popular times found, ready to scrap!")
#                 print("==============================================================")
#                 break
#     except TimeoutException:
#         print("Oops, sorry wrong website!")
#         print("===========================================")
#         print("Attempting to get a right website!")
#         self.driver.quit()
#         self.driver = webdriver.Chrome(service=self.service)
#         continue
