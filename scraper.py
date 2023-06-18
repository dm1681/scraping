import requests
import time


from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

URL = "https://www.aloyoga.com/collections/yoga-mats"
driver = webdriver.Edge()


# go to the url and wait for the website to load
driver.get(URL)
time.sleep(5)

elem = driver.find_element(by=By.CLASS_NAME, value="product-cards")
products = elem.find_elements(by=By.CLASS_NAME, value="PlpTile " )

def find_reviews(driver:webdriver.Edge) -> WebElement:
    try:
        reviews_div = driver.find_element(by=By.CLASS_NAME, value="yotpo-reviews yotpo-active")
        return reviews_div
    except NoSuchElementException as e:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(3)
        reviews_div = find_reviews(driver)
        return reviews_div
        

        




# add checks for modals...
for product in products[:1]:
    info_div = product.find_element(by=By.CLASS_NAME, value="info")
    product_name_div = info_div.find_element(by=By.CLASS_NAME, value="product-name")
    product_link = product_name_div.find_element(by=By.TAG_NAME, value="a")
    product_name = product_link.text
    if product_name.find("Warrior") != -1:
        product.click()
        time.sleep(5)

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
        



    


