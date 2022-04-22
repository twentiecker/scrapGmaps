from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time


class WebDriver:
    location_data = {}

    def __init__(self):
        # The __init__ function is the constructor that will automatically get called and initialize
        # these necessary parameters.

        service = ChromeService(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)

        self.location_data["rating"] = "NA"
        self.location_data["reviews_count"] = "NA"
        self.location_data["location"] = "NA"
        self.location_data["contact"] = "NA"
        self.location_data["website"] = "NA"
        self.location_data["Time"] = {"Senin": "NA", "Selasa": "NA", "Rabu": "NA", "Kamis": "NA",
                                      "Jumat": "NA", "Sabtu": "NA", "Minggu": "NA"}
        self.location_data["Popular Times"] = {"Senin": [], "Selasa": [], "Rabu": [], "Kamis": [],
                                               "Jumat": [], "Sabtu": [], "Minggu": []}
        self.location_data["Reviews"] = []

        # print(self.location_data['Popular Times']['Monday'])  # access object

    def get_location_data(self):
        # The self.driver.find_element are the Selenium functions that automatically find out the
        # HTML elements with that class name or id name and stores them into a variable, and later we can use
        # the text() function over those variables to get the respective values.

        avg_rating = self.driver.find_element(By.CLASS_NAME, "fontDisplayLarge")
        total_reviews = self.driver.find_element(By.CLASS_NAME, "h0ySl-wcwwM-E70qVe")
        address = self.driver.find_element(By.XPATH,
                                           "//*[@id='pane']/div/div[1]/div/div/div[9]/div[1]/button/div[1]/div[2]/div[1]")
        phone_number = self.driver.find_element(By.XPATH,
                                                "//*[@id='pane']/div/div[1]/div/div/div[9]/div[5]/button/div[1]/div[2]/div[1]")
        website = self.driver.find_element(By.XPATH,
                                           "//*[@id='pane']/div/div[1]/div/div/div[9]/div[4]/button/div[1]/div[2]/div[1]")

        self.location_data["rating"] = avg_rating.text.strip()
        self.location_data["reviews_count"] = total_reviews.text.replace("ulasan", ""). \
            replace("reviews", "").strip()
        self.location_data["location"] = address.text.strip()
        self.location_data["contact"] = phone_number.text.strip()
        self.location_data["website"] = website.text.strip()

    def click_open_close_time(self):
        if len(list(self.driver.find_elements(By.CLASS_NAME, "LJKBpe-Tswv1b-hour-text"))) != 0:
            element = self.driver.find_element(By.CLASS_NAME, "LJKBpe-Tswv1b-hour-text")
            self.driver.implicitly_wait(5)
            ActionChains(self.driver).move_to_element(element).click(element).perform()

    def get_location_open_close_time(self):
        # The class “lo7U087hsMA__row-header” contains all the days and “lo7U087hsMA__row-interval”
        # contains the respective open and close times.

        # It will be a list containing all HTML section the days names.
        days = self.driver.find_elements(By.CLASS_NAME, "ylH6lf")
        # It will be a list with HTML section of open and close time for the respective day.
        times = self.driver.find_elements(By.CLASS_NAME, "y0skZc-t0oSud")

        # Getting the text(day name) from each HTML day section.
        day = [a.text for a in days]
        # Getting the text(open and close time) from each HTML open and close time section.
        open_close_time = [a.text for a in times]

        for i, j in zip(day, open_close_time):
            self.location_data["Time"][i] = j

    def get_popular_times(self):
        # The class that will get all the days and for each day finds out the busy percentage for each hour in a day
        # of the location.
        #
        # The variable “a” is a list of all the days, then we loop through “a” and find out all the times available
        # in that day and store it into list “b”, then loop in b and find out the busy percentage for that respective
        # hour in a day and store it in our final data list.

        # It will be a List of the HTML Section of each day.
        a = self.driver.find_elements(By.CLASS_NAME, "g2BVhd eoFzo")
        dic = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}
        l = {"Sunday": [], "Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": [],
             "Saturday": []}
        count = 0

        for i in a:
            b = i.find_elements_by_class_name(
                "dpoVLd")  # It will be a list of HTML Section of each hour in a day.
            for j in b:
                x = j.get_attribute(
                    "aria-label")  # It gets the busy percentage value from HTML Section of each hour.
                l[dic[count]].append(x)
            count = count + 1

        for i, j in l.items():
            self.location_data["Popular Times"][i] = j

    def scrape(self, url):  # Passed the URL as a variable
        try:
            # Get is a method that will tell the driver to open at that particular URL
            self.driver.get(url)
        except Exception as e:
            self.driver.quit()
            return

        time.sleep(10)  # Waiting for the page to load.

        self.get_location_data()  # Calling the function to get all the location data.
        self.click_open_close_time()  # Calling the function to click the open and close time button.
        self.get_location_open_close_time()  # Calling to get open and close time for each day.
        # self.get_popular_times()  # Gets the busy percentage for each hour of each day.

        # Clicking the all reviews button and redirecting the driver to the all reviews page.
        # if (self.click_all_reviews_button() == False):
        #     return (self.location_data)

        time.sleep(5)  # Waiting for the all reviews page to load.

        # self.scroll_the_page()  # Scrolling the page to load all reviews.
        # self.expand_all_reviews()  # Expanding the long reviews by clicking see more button in each review.
        # self.get_reviews_data()  # Getting all the reviews data.

        self.driver.quit()  # Closing the driver instance.

        return (self.location_data)  # Returning the Scraped Data.


url = "https://www.google.co.id/maps/place/Bogor+Cafe/@-6.172172,106.8266993,15z/data=!4m9!1m2!2m1!1srestaurant+or+cafe!3m5!1s0x2e69f5cc0abf0f67:0x78dce6deb9815e6!8m2!3d-6.172172!4d106.835454!15sChJyZXN0YXVyYW50IG9yIGNhZmVaFCIScmVzdGF1cmFudCBvciBjYWZlkgEVaW5kb25lc2lhbl9yZXN0YXVyYW50mgEkQ2hkRFNVaE5NRzluUzBWSlEwRm5TVVI1TFdWUFVISlJSUkFC"
x = WebDriver()
print(x.scrape(url))
