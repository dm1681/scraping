import os
import time
from pathlib import Path

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# URL = "https://www.aloyoga.com/collections/yoga-mats"
URL = "https://www.aloyoga.com/collections/yoga-gear?ProductType=Accessories%3AEquipment%3ATowel"
OUTPUT_PATH = Path("./output.txt")

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

def find_reviews(driver:webdriver.Chrome, scroll_height:int=50) -> WebElement:
    try:
        reviews_div = driver.find_element(by=By.ID, value="reviews-summary")
        return reviews_div
    except NoSuchElementException:
        print("Didnt find reviews div. Scrolling down...")
        dy = 2000
        driver.execute_script(f"window.scrollTo(0, {scroll_height})")
        time.sleep(1.5)
        reviews_div = find_reviews(driver, scroll_height=scroll_height+dy)
        return reviews_div
        

        

def check_modal(driver:webdriver.Chrome):
    # check for the presence of the a modal
    modals = driver.find_elements(by=By.CLASS_NAME, value="alo-modal-scroller")
    if len(modals) > 0:
        # just find any element and click i guess?
        modal_backdrop = driver.find_element(by=By.CLASS_NAME, value="declineOffer")
        modal_backdrop.click()



data = ""
for idx, product in enumerate(products[:1]):
    # get the first product
    info_div = product.find_element(by=By.CLASS_NAME, value="info")
    product_name_div = info_div.find_element(by=By.CLASS_NAME, value="product-name")
    product_link = product_name_div.find_element(by=By.TAG_NAME, value="a")
    product_name = product_link.text

    # verify we have the right product
    if product_name.find("Towel") != -1:
        print(f"Clicking {idx} product")
        product.click()
        time.sleep(2)
        check_modal(driver)

        # now we go to reviews
        goto_reviews = driver.find_element(by=By.CLASS_NAME, value="ReviewsBottomLine")
        goto_reviews.click()

        

        
        while True:

            # handle review pages
            active_review_page = int(driver.find_element(by=By.CSS_SELECTOR, value="a.yotpo-page-element.goTo.yotpo-active").text)
            next_review_page_arrow = driver.find_element(by=By.CSS_SELECTOR, value="a.yotpo-page-element.yotpo-icon.yotpo-icon-right-arrow.yotpo_next")
            print(f"Reading review page {active_review_page}")

            # get reviews div
            reviews_div = driver.find_element(by=By.ID, value="Yotpo-Reviews")
            review_divs = reviews_div.find_elements(by=By.CLASS_NAME, value = "yotpo-review")

            # iterate over reviews and print them
            for review_div in review_divs:
                # parse review content
                review_main = review_div.find_element(by=By.CLASS_NAME, value="yotpo-main ")
                review_header = review_div.find_element(by=By.CLASS_NAME, value="yotpo-header")
                review_header_element = review_header.find_elements(by=By.CLASS_NAME, value="yotpo-header-element")[1]
                review_stars_div= review_header.find_element(by=By.CSS_SELECTOR, value="div.yotpo-review-stars")
                review_stars = review_stars_div.find_elements(by=By.CLASS_NAME, value="yotpo-icon-star")
                n_stars = len(review_stars)

                review_main_content_div = review_main.find_element(by=By.CLASS_NAME, value="yotpo-review-wrapper")
                review_content = review_main_content_div.find_element(by=By.CLASS_NAME, value="content-review")
                review_content = review_content.text
                review_data = f"{n_stars}\t{review_content}\n"
                data += review_data
                print(review_data)
                # review_footer = review_div.find_element(by=By.CLASS_NAME, value="yotpo-footer ")

            # update prev and active so we can know when to stop
            prev_review_page = active_review_page

            # click arrow
            print("moving next arrow into screen")
            driver.execute_script("arguments[0].scrollIntoView();", next_review_page_arrow)
            time.sleep(1)
            print("clicking next arrow")
            next_review_page_arrow.click()
            print("clicked next arrow... waiting...")
            time.sleep(3)

            # get active review page and compare to see if we are at the end
            active_review_page = int(driver.find_element(by=By.CSS_SELECTOR, value="a.yotpo-page-element.goTo.yotpo-active").text)
            print(f"{active_review_page = }\t{prev_review_page = }")

            if prev_review_page == active_review_page:
                break


        
        print("finished :)")


with open(OUTPUT_PATH, "w") as f:
    f.write(data)
    


