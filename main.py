# I want to make a program that can automatically visit scihub and download the paper I want.

import requests
import time
from selenium import webdriver


# 1. Open the website
# 2. Input the paper's title
# 3. Click the search button
# 4. Click the download button
# 5. Download the paper
# 6. Close the website


# 1. Open the website
def open_website():
    url = 'https://sci-hub.se/'
    driver = webdriver.Chrome()
    driver.get(url)
    return driver


# 2. Input the paper's title
def input_title(driver, title):
    # driver.find_element_by_id is not avaliable now
    #time.sleep(30)
    input = driver.find_element("id", "request")
    input.send_keys(title)


# 3. Click the search button
def click_search(driver):
    # <button type="submit"><img src="/pictures/key.png"><span>查询</span></button>
    # the html code above is the code of the search button

    search = driver.find_element("xpath", "//button[@type='submit']")
    search.click()
    # time.sleep(2)


# 4. Click the download button and save to the desktop
def click_download(driver):
    try:
        download = driver.find_element("xpath", "//button[@onclick]")
        download.click()
        time.sleep(3)
        print("Download successfully, please check your \"download!\" folder!")
    # if the paper is not exist
    except:
        print("The paper is not exist!")

# 5. Close the website
def close_website(driver):
    driver.close()


# 7. Main function
def main():
    while True:
        website = input("Please input doi / website of the paper you want to download: ")
        driver = open_website()
        input_title(driver, website)
        click_search(driver)
        click_download(driver)
        close_website(driver)


main()
