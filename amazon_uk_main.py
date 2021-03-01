from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import timeit


amazon = []
url_list = ['https://www.amazon.co.uk/s?k=macbook+pro&ref=nb_sb_noss_1']


def main_settings():
    proxy = "196.244.200.54:12345"
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=' + proxy)
    options.add_argument('headless')
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    start_time = timeit.default_timer()
    for i in range(1, 7):
        url = url_list[-1]
        settings_driver(url, driver)
    end_time = timeit.default_timer()
    print(end_time-start_time)
    make_csv_file()


def settings_driver(url, driver):
    driver.get(url)
    time.sleep(3)
    url_list.append(driver.find_element_by_class_name('a-pagination').find_element_by_class_name('a-last').
      find_element_by_tag_name('a').get_attribute('href'))
    scrap_data(driver)


def scrap_data(driver):
    tab = driver.find_elements_by_class_name('s-asin')
    for item in tab:
        table = {}
        try:
            table['Price'] = item.find_element_by_class_name('a-price-whole').text  
        except NoSuchElementException:
            table['Price'] = 'NO price'
        table['Title'] = item.find_element_by_class_name('a-size-medium').text 
        table['URL Product'] = item.find_element_by_class_name('a-link-normal').get_attribute('href')  
        try:
            rating = item.find_element_by_class_name('a-icon-alt').get_attribute('innerText') 
            global_rating = item.find_element_by_class_name('a-size-base').text  
            table['Rating'] = f"{rating} - {global_rating}"
        except NoSuchElementException:
            table['Rating'] = 'NO'
        table['URL Of Pic'] = item.find_element_by_tag_name('img').get_attribute('src') 

        amazon.append(table)


def make_csv_file():
    df = pd.DataFrame(amazon)
    df.to_csv('AMAZON.csv', encoding='utf-8-sig', index=False)


main_settings()
