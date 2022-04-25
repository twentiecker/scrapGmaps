from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
import time
import main

url = "https://www.google.co.id/maps/search/restaurant+or+cafe/@-6.1721719,106.8266993,15z/data=!3m1!4b1"

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get(url)

# Waits for the page to load.
WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, 'hfpxzc')))

pause_time = 2  # Waiting time after each scroll.

# It gets the section of the scroll bar.
container = driver.find_elements(By.CLASS_NAME, 'm6QErb')
scrollable_div = container[2]

while (True):
    x = 0
    while (True):
        # Get initial total of card
        cards = driver.find_elements(By.CLASS_NAME, 'bfdHYd')

        # Scroll it to the bottom.
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)

        time.sleep(pause_time)  # wait for more reviews to load.

        # Break the loop if nothing change in cards total
        if x == len(cards):
            break

        # Set temporary value for cards total gained
        x = len(cards)
        print(x)

    # Get all link of detail page
    detail_page = driver.find_elements(By.CLASS_NAME, "hfpxzc")

    # Click every detail page
    a = 2
    for a in range(3):
        print(detail_page[a])
        time.sleep(3)
        # WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, 'hfpxzc')))
        detail_page[a].click()
        time.sleep(10)
        driver.find_element(By.CLASS_NAME, 'xoLGzf-icon').click()
        a = a+1

    btn = driver.find_elements(By.CLASS_NAME, "hV1iCc")
    for i in btn:
        j = i.get_attribute("jsaction")
        if j == "pane.paginationSection.nextPage":
            i.click(i)
            break
    print("===========================================================")
    time.sleep(3)

# // *[ @ id = "pane"] / div / div[1] / div / div / div[2] / div[1] / div[3] / div / a
# 1
# // *[ @ id = "pane"] / div / div[1] / div / div / div[2] / div[1] / div[5] / div / a
# 2
# // *[ @ id = "pane"] / div / div[1] / div / div / div[2] / div[1] / div[7] / div / a
# 3
# // *[ @ id = "pane"] / div / div[1] / div / div / div[2] / div[1] / div[9] / div / a
# 4
#
# // *[ @ id = "pane"] / div / div[1] / div / div / div[2] / div[1] / div[41] / div / a
# 20

# //*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[41]/div/a
