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


class WebDriver:
    location_data = {}

    def __init__(self):
        # The __init__ function is the constructor that will automatically get called and initialize
        # these necessary parameters.

        service = ChromeService(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)

        self.location_data["title"] = "NA"
        # self.location_data["rating"] = "NA"
        # self.location_data["reviews_count"] = "NA"
        self.location_data["price_cat"] = "NA"
        self.location_data["price_desc"] = "NA"
        self.location_data["location"] = "NA"
        # self.location_data["contact"] = "NA"
        # self.location_data["website"] = "NA"
        # self.location_data["Time"] = {"Senin": "NA", "Selasa": "NA", "Rabu": "NA", "Kamis": "NA",
        #                               "Jumat": "NA", "Sabtu": "NA", "Minggu": "NA"}
        self.location_data["Popular Times"] = {"Senin": [], "Selasa": [], "Rabu": [], "Kamis": [],
                                               "Jumat": [], "Sabtu": [], "Minggu": []}
        # self.location_data["Reviews"] = []

        # print(self.location_data['Popular Times']['Monday'])  # access object

    def get_location_data(self):
        # The self.driver.find_element are the Selenium functions that automatically find out the
        # HTML elements with that class name or id name and stores them into a variable, and later we can use
        # the text() function over those variables to get the respective values.

        title = self.driver.find_element(By.CLASS_NAME,'DUwDvf')
        # avg_rating = self.driver.find_element(By.CLASS_NAME, "fontDisplayLarge")
        # total_reviews = self.driver.find_element(By.CLASS_NAME, "h0ySl-wcwwM-E70qVe")
        container_price = self.driver.find_element(By.CLASS_NAME, 'mgr77e')
        tag_price = container_price.find_elements(By.TAG_NAME, 'span')
        for i in tag_price:
            label = i.get_attribute("aria-label")
            if label:
                price_cat = i.text
                price_desc = label

        tag_address = self.driver.find_elements(By.CLASS_NAME, 'CsEnBe')
        for i in tag_address:
            label = i.find_element(By.TAG_NAME, 'img')
            if label.get_attribute('src') == "https://maps.gstatic.com/mapfiles/maps_lite/images/2x/ic_plus_code.png":
                address = i.find_element(By.CLASS_NAME, 'Io6YTe')

        # Get province of address
        prov = address.text.strip().split(sep=",")

        # phone_number = self.driver.find_element(By.XPATH,
        #                                         "//*[@id='pane']/div/div[1]/div/div/div[9]/div[5]/button/div[1]/div[2]/div[1]")
        # website = self.driver.find_element(By.XPATH,
        #                                    "//*[@id='pane']/div/div[1]/div/div/div[9]/div[4]/button/div[1]/div[2]/div[1]")

        # self.location_data["rating"] = avg_rating.text.strip()
        # self.location_data["reviews_count"] = total_reviews.text.replace("ulasan", ""). \
        #     replace("reviews", "").strip()
        self.location_data["title"] = title.text.strip()
        self.location_data["price_cat"] = price_cat.strip()
        self.location_data["price_desc"] = price_desc.replace(":", "").strip()
        self.location_data["location"] = prov[2].strip()
        # self.location_data["contact"] = phone_number.text.strip()
        # self.location_data["website"] = website.text.strip()

    # def click_open_close_time(self):
    #     if len(list(self.driver.find_elements(By.CLASS_NAME, "LJKBpe-Tswv1b-hour-text"))) != 0:
    #         element = self.driver.find_element(By.CLASS_NAME, "LJKBpe-Tswv1b-hour-text")
    #         self.driver.implicitly_wait(5)
    #         ActionChains(self.driver).move_to_element(element).click(element).perform()

    # def get_location_open_close_time(self):
    #     # The class “lo7U087hsMA__row-header” contains all the days and “lo7U087hsMA__row-interval”
    #     # contains the respective open and close times.
    #
    #     # It will be a list containing all HTML section the days names.
    #     days = self.driver.find_elements(By.CLASS_NAME, "ylH6lf")
    #
    #     # It will be a list with HTML section of open and close time for the respective day.
    #     times = self.driver.find_elements(By.CLASS_NAME, "y0skZc-t0oSud")
    #
    #     # Getting the text(day name) from each HTML day section.
    #     day = [a.text for a in days]
    #
    #     # Getting the text(open and close time) from each HTML open and close time section.
    #     open_close_time = [a.text for a in times]
    #
    #     for i, j in zip(day, open_close_time):
    #         self.location_data["Time"][i] = j

    def get_popular_times(self):
        # The class that will get all the days and for each day finds out the busy percentage for each hour in a day
        # of the location.
        # The variable “a” is a list of all the days, then we loop through “a” and find out all the times available
        # in that day and store it into list “b”, then loop in b and find out the busy percentage for that respective
        # hour in a day and store it in our final data list.

        # It will be a List of the HTML Section of each day.
        a = self.driver.find_elements(By.CLASS_NAME, "g2BVhd")

        dic = {0: "Minggu", 1: "Senin", 2: "Selasa", 3: "Rabu", 4: "Kamis", 5: "Jumat", 6: "Sabtu"}
        l = {"Minggu": [], "Senin": [], "Selasa": [], "Rabu": [], "Kamis": [], "Jumat": [], "Sabtu": []}
        count = 0

        for i in a:
            # It will be a list of HTML Section of each hour in a day.
            b = i.find_elements(By.CLASS_NAME, "dpoVLd")

            for j in b:
                # It gets the busy percentage value from HTML Section of each hour.
                x = j.get_attribute("aria-label")

                l[dic[count]].append(x)
            count = count + 1

        for i, j in l.items():
            self.location_data["Popular Times"][i] = j

    # def click_reviews_button(self):
    #     # Find the All reviews button on the HTML and use the selenium .click() function to click it and get
    #     # redirected to that page.
    #
    #     WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.CLASS_NAME, "M77dve")))
    #
    #     element = self.driver.find_elements(By.CLASS_NAME, "M77dve")
    #     for i in element:
    #         j = i.get_attribute("aria-label")
    #         if "Ulasan lainnya" in j:
    #             i.click()
    #             break

    # def scroll_the_page(self):
    #     # Gmaps like most other modern websites is implemented using AJAX which means the rest of
    #     # the reviews will only be loaded into HTML when you scroll down to look at them.
    #     #
    #     # Scroll page function that will first scroll and load all the reviews before we further proceed
    #     # to scrape reviews.
    #
    #     # Waits for the page to load.
    #     WebDriverWait(self.driver, 10).until(
    #         ec.presence_of_element_located((By.XPATH, '//*[@id="pane"]/div/div[1]/div/div/div[2]')))
    #
    #     pause_time = 2  # Waiting time after each scroll.
    #     max_count = 5  # Number of times we will scroll the scroll bar to the bottom.
    #     x = 0
    #
    #     while (x < max_count):
    #         # It gets the section of the scroll bar.
    #         scrollable_div = self.driver.find_element(By.XPATH, '//*[@id="pane"]/div/div[1]/div/div/div[2]')
    #
    #         # Scroll it to the bottom.
    #         self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
    #
    #         time.sleep(pause_time)  # wait for more reviews to load.
    #         x = x + 1

    # def expand_all_reviews(self):
    #     # To see the long reviews we have to click the more button under each review to make it load into the Html.
    #     #
    #     # Expand all reviews function that will find all these more buttons on the already loaded page and clicks
    #     # them to load the entire reviews.
    #
    #     element = self.driver.find_elements(By.CLASS_NAME, "w8nwRe")
    #     for i in element:
    #         i.click()

    # def get_reviews_data(self):
    #     # Now that everything is been loaded we will create a function that scrapes the reviews data like
    #     # each reviewer name, text, posted date, and rating.
    #
    #     review_names = self.driver.find_elements(By.CLASS_NAME,
    #                                              "d4r55")  # Its a list of all the HTML sections with the reviewer name.
    #     review_text = self.driver.find_elements(By.CLASS_NAME,
    #                                             "wiI7pd")  # Its a list of all the HTML sections with the reviewer reviews.
    #     review_dates = self.driver.find_elements(By.CLASS_NAME,
    #                                              "rsqaWe")  # Its a list of all the HTML sections with the reviewer reviewed date.
    #     review_stars = self.driver.find_elements(By.CLASS_NAME,
    #                                              "kvMYJc")  # Its a list of all the HTML sections with the reviewer rating.
    #
    #     review_stars_final = []
    #
    #     for i in review_stars:
    #         review_stars_final.append(i.get_attribute("aria-label"))
    #
    #     review_names_list = [a.text for a in review_names]
    #     review_text_list = [a.text for a in review_text]
    #     review_dates_list = [a.text for a in review_dates]
    #     review_stars_list = [a for a in review_stars_final]
    #
    #     for (a, b, c, d) in zip(review_names_list, review_text_list, review_dates_list, review_stars_list):
    #         self.location_data["Reviews"].append({"name": a, "review": b, "date": c, "rating": d})

    def scrape(self, url):  # Passed the URL as a variable
        while (True):
            try:
                # Get is a method that will tell the driver to open at that particular URL
                self.driver.get(url)

                # Waiting for the page to load element "rating"
                WebDriverWait(self.driver, 20).until(
                    ec.presence_of_element_located((By.XPATH, '//*[@id="pane"]/div/div[1]/div/div')))
                print("Element found, ready to scrap!")
                print("==============================================================")
                break
            except TimeoutException:
                self.driver.get(url)
                print("Sorry website not available!")

        self.get_location_data()  # Calling the function to get all the location data.
        # self.click_open_close_time()  # Calling the function to click the open and close time button.
        # self.get_location_open_close_time()  # Calling to get open and close time for each day.
        self.get_popular_times()  # Gets the busy percentage for each hour of each day.

        # Clicking the all reviews button and redirecting the driver to the all reviews page.
        # self.click_reviews_button()

        # time.sleep(5)  # Waiting for the all reviews page to load.

        # self.scroll_the_page()  # Scrolling the page to load all reviews.
        # self.expand_all_reviews()  # Expanding the long reviews by clicking see more button in each review.
        # self.get_reviews_data()  # Getting all the reviews data.

        self.driver.quit()  # Closing the driver instance.

        return (self.location_data)  # Returning the Scraped Data.


url = "https://www.google.co.id/maps/place/Bogor+Cafe/@-6.172172,106.8266993,15z/data=!4m9!1m2!2m1!1srestaurant+or+cafe!3m5!1s0x2e69f5cc0abf0f67:0x78dce6deb9815e6!8m2!3d-6.172172!4d106.835454!15sChJyZXN0YXVyYW50IG9yIGNhZmVaFCIScmVzdGF1cmFudCBvciBjYWZlkgEVaW5kb25lc2lhbl9yZXN0YXVyYW50mgEkQ2hkRFNVaE5NRzluUzBWSlEwRm5TVVI1TFdWUFVISlJSUkFC"
x = WebDriver()
print(x.scrape(url))
