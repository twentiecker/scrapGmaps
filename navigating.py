from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
import time


class Navigating():
    def __init__(self, driver, url):
        self.driver = driver
        self.max_count = 0
        self.url = url

    def prerequisite_home(self):
        try:
            # Check visibility of pagination
            WebDriverWait(self.driver, 20).until(ec.presence_of_element_located(
                (By.CSS_SELECTOR, "button[jsaction='pane.paginationSection.nextPage']")))
            print("*** Prerequisite check for home page is satisfied ***")
        except TimeoutException:
            print("*** Prerequisite check for home page is not satisfied ***")
            print("*** Attempting to re-open the website ***")
            self.driver.quit()
            time.sleep(3)  # give time for re-opening web after closing it
            self.driver.get(self.url)
            time.sleep(5)  # wait for completed page loaded
            self.prerequisite_home()

    def scroll_home(self):
        x = 0
        tag_scrollable = self.driver.find_element(By.CSS_SELECTOR, "div[role='main']")
        label = tag_scrollable.find_elements(By.CLASS_NAME, 'm6QErb')

        for i in label:
            if i.get_attribute('aria-label'):
                scrollable_div = i
                break

        while True:
            container_items = self.driver.find_elements(By.CLASS_NAME, 'Nv2PK')
            self.max_count = len(container_items)
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
            time.sleep(2)  # wait for more items to load.
            if x == self.max_count:
                break
            x = self.max_count

    def click_items_home(self, i):
        WebDriverWait(self.driver, 20).until(ec.visibility_of_element_located((By.CLASS_NAME, "hfpxzc")))
        items = self.driver.find_elements(By.CLASS_NAME, 'hfpxzc')
        ActionChains(self.driver).move_to_element(items[i]).perform()
        time.sleep(1)
        ActionChains(self.driver).move_to_element(items[i]).click(items[i]).perform()

    def prerequisite_detail(self):
        try:
            # Check whether the page has "popular times" element
            if WebDriverWait(self.driver, 5).until(ec.presence_of_element_located((By.CLASS_NAME, 'g2BVhd'))):
                list_class = ['DUwDvf', 'skqShb', 'CsEnBe']
                for i in range(3):
                    WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.CLASS_NAME, list_class[i])))
        except TimeoutException:
            time.sleep(3)
            self.back_to_home()

    def back_to_detail(self):
        WebDriverWait(self.driver, 20).until(ec.visibility_of_element_located((By.CLASS_NAME, "VfPpkd-icon-LgbsSe")))
        btn = self.driver.find_element(By.CLASS_NAME, 'VfPpkd-icon-LgbsSe')
        ActionChains(self.driver).move_to_element(btn).perform()
        time.sleep(1)
        ActionChains(self.driver).move_to_element(btn).click(btn).perform()

    def back_to_home(self):
        WebDriverWait(self.driver, 20).until(ec.visibility_of_element_located((By.CLASS_NAME, "hYBOP")))
        btn = self.driver.find_element(By.CLASS_NAME, 'hYBOP')
        ActionChains(self.driver).move_to_element(btn).perform()
        time.sleep(1)
        ActionChains(self.driver).move_to_element(btn).click(btn).perform()
