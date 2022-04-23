from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
import time

# url = "https://www.google.co.id/maps/search/bengkel/@-6.1721719,106.8266993,15z/data=!3m1!4b1"
url = "https://www.google.co.id/maps/search/restaurant+or+cafe/@-6.1721719,106.8266993,15z/data=!3m1!4b1"
# url = "https://www.google.co.id/maps/search/toko+baju/@-6.1721719,106.8266993,15z/data=!3m1!4b1"
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get(url)

# Waits for the page to load.
WebDriverWait(driver, 10).until(
    ec.presence_of_element_located((By.CLASS_NAME, 'hfpxzc')))

pause_time = 2  # Waiting time after each scroll.
max_count = 5  # Number of times we will scroll the scroll bar to the bottom.
x = 0

# It gets the section of the scroll bar.
container = driver.find_elements(By.CLASS_NAME, 'm6QErb')
scrollable_div = container[2]

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

btn = driver.find_elements(By.CLASS_NAME,"hV1iCc")
for i in btn:
    j = i.get_attribute("jsaction")
    if j == "pane.paginationSection.nextPage":
        ActionChains(driver).move_to_element(i).click(i).perform()
        break

time.sleep(10)