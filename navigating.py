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


class Navigating():
    def __init__(self, driver):
        self.driver = driver

    def prerequisite_home(self):
        try:
            # Check pagination
            WebDriverWait(self.driver, 20).until(ec.presence_of_element_located(
                (By.CSS_SELECTOR, "button[jsaction='pane.paginationSection.nextPage']")))
        except:
            self.driver.refresh()

    def prerequisite_detail(self, i):
        try:
            # Waiting for the page to load element "popular times"
            WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.CLASS_NAME, 'g2BVhd')))
        except TimeoutException:
            self.click_items_home(i)

    def click_items_home(self, i):
        items = self.driver.find_elements(By.CLASS_NAME, 'hfpxzc')
        items[i].click()

    def back_to_detail(self):
        # Back to detail page from review page
        self.driver.find_element(By.CLASS_NAME, 'VfPpkd-icon-LgbsSe').click()

    def back_to_home(self):
        # Back to home page from detail page
        self.driver.find_element(By.CLASS_NAME, 'hYBOP').click()

    def scrap_detail(self):
        url = "https://www.google.co.id/maps/search/restaurant+or+cafe/@-6.1721719,106.8266993,15z/data=!3m1!4b1"

        service = ChromeService(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.get(url)

        # Waits for the page to load.
        WebDriverWait(driver, 20).until(ec.presence_of_element_located((By.CLASS_NAME, 'hfpxzc')))

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
            list_v = []
            for u in detail_page:
                v = u.get_attribute('href')
                list_v.append(v)

            # Click every detail page
            a = 2
            for a in range(3):
                if a == 2:
                    container = driver.find_elements(By.CLASS_NAME, 'm6QErb')
                    scrollable_div = container[2]
                    o = 1
                    while True:
                        # driver.refresh()
                        # Get initial total of card
                        # cards = driver.find_elements(By.CLASS_NAME, 'bfdHYd')

                        # Scroll it to the bottom.
                        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)

                        time.sleep(pause_time)  # wait for more reviews to load.

                        # Break the loop if nothing change in cards total
                        if o == 2:
                            break
                        o = o + 1
                        # Set temporary value for cards total gained
                        # x = len(cards)
                        # print(x)

                # print(list_v[a])
                time.sleep(3)
                # WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, 'hfpxzc')))
                # detail_page[a].click()
                # t = detail_page[a].get_attribute('href')
                t = list_v[a]
                print(t)
                driver.get(t)
                time.sleep(10)
                # driver.find_element(By.CLASS_NAME, 'xoLGzf-icon').click()
                driver.back()
                a = a + 1

            btn = driver.find_elements(By.CLASS_NAME, "hV1iCc")
            for i in btn:
                j = i.get_attribute("jsaction")
                if j == "pane.paginationSection.nextPage":
                    i.click()
                    break
            print("===========================================================")
            time.sleep(3)
