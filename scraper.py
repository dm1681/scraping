import os
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

URL = "https://www.aloyoga.com/collections/yoga-mats"

#setup chrome options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")

homedir = os.path.expanduser("~")
webdriver_service = Service(f"{homedir}/chromedriver/stable/chromedriver")

driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)


# go to the url and wait for the website to load
driver.get(URL)
time.sleep(5)

elem = driver.find_element(by=By.CLASS_NAME, value="product-cards")
products = elem.find_elements(by=By.CLASS_NAME, value="PlpTile " )

def find_reviews(driver:webdriver.Chrome) -> WebElement:
    try:
        reviews_div = driver.find_element(by=By.CLASS_NAME, value="yotpo-reviews yotpo-active")
        return reviews_div
    except NoSuchElementException:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(3)
        reviews_div = find_reviews(driver)
        return reviews_div
        

        

def check_modal(driver:webdriver.Chrome):
    # check for the presence of the a modal

    modals = driver.find_elements(by=By.CLASS_NAME, value="alo-modal-scroller")
    if len(modals) > 0:
        close_button = modals[0].find_element(by=By.CLASS_NAME, value="alo-modal-close-icon::after")
        close_button.click()



# add checks for modals...
for product in products[:1]:
    info_div = product.find_element(by=By.CLASS_NAME, value="info")
    product_name_div = info_div.find_element(by=By.CLASS_NAME, value="product-name")
    product_link = product_name_div.find_element(by=By.TAG_NAME, value="a")
    product_name = product_link.text
    if product_name.find("Warrior") != -1:
        product.click()
        time.sleep(5)
        check_modal(driver)

        # now we go to reviews

        reviews_div = find_reviews(driver)
        
        review_divs = reviews_div.find_elements(by=By.CLASS_NAME, value = "yotpo-review yotpo-regular-box  ")
        for review_div in review_divs:
            # parse review content
            review_main = review_div.find_element(by=By.CLASS_NAME, value="yotpo-main ")
            review_main_content_div = review_main.find_element(by=By.CLASS_NAME, value="yotpo-review-wrapper")
            review_content = review_main_content_div.find_element(by=By.CLASS_NAME, value="content-review")
            review_content = review_content.text
            print(review_content)
            # review_footer = review_div.find_element(by=By.CLASS_NAME, value="yotpo-footer ")
        



    


