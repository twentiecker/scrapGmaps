from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time


class Scrolling:
    def __init__(self):
        self.page_soup = ""
        # self.page_soup_lv3 = ""

    def scroll(self, url):
        service = ChromeService(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.get(f"{url}")
        time.sleep(2)  # Allow 2 seconds for the web page to open
        self.page_soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.close()

    # def scroll_lv3(self, category):
    #     service = ChromeService(executable_path=ChromeDriverManager().install())
    #     driver = webdriver.Chrome(service=service)
    #     driver.get(f"https://www.gojek.com/{category.lower()}")
    #     time.sleep(2)  # Allow 2 seconds for the web page to open
    #     self.page_soup_lv3 = BeautifulSoup(driver.page_source, "html.parser")
    #     driver.close()
