# I want to make a program that can automatically visit scihub and download the paper I want.
import time
from selenium import webdriver
import PySimpleGUI as sg


def initialization():
    # set the specific text size in PySimpleGUI
    sg.SetOptions(text_justification="center", font=("Times New Roman", 15))
    # set the theme of the window, color should be formal
    sg.theme("LightBrown1")

    # set the layout of the window
    layout = [[sg.Text("Status"), sg.Text("DOI Not Provided", key="status", text_color="red")],
              [sg.Text("Please input doi / website of the paper you want to download: ")],
              [sg.Input(key="website")],
              [sg.Button("OK"), sg.Button("Cancel")]]

    # create the window
    window = sg.Window("Download Paper", layout)
    return window


def window_operation(window):
    while True:
        event, values = window.read()
        if event in (None, "Cancel"):
            # end the program
            exit()
        if event == "OK":
            # change the status
            window["status"].update("Downloading, please wait for 5 seconds...", text_color="green")
            # update the window
            window.refresh()
            break
    return values


# 1. Open the website
# 2. Input the paper's title
# 3. Click the search button
# 4. Click the download button
# 5. Download the paper
# 6. Close the website


# 1. Open the website
def open_website():
    op = webdriver.ChromeOptions()
    op.add_argument('headless')  # not showing up the browser

    # set the path to download
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': "C:\\Users\\74483\\Downloads"}
    op.add_experimental_option('prefs', prefs)

    url = 'https://sci-hub.se/'
    driver = webdriver.Chrome(options=op)
    driver.get(url)
    return driver


# 2. Input the paper's title
def input_title(driver, title):
    # driver.find_element_by_id is not avaliable now
    # time.sleep(30)
    in_put = driver.find_element("id", "request")
    in_put.send_keys(title)


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
        # print("Download successfully, please check your \"download!\" folder!")
        sg.Popup("Download successfully, please check your \"download!\" folder!")
    # if the paper is not exist
    except:
        # print("The paper is not exist!")
        sg.Popup("The paper does not exist!")


# 5. Close the website
def close_website(driver):
    driver.close()


# 7. Main function
def main():
    while True:
        window = initialization()
        values = window_operation(window)
        # website = input("Please input doi / website of the paper you want to download: ")
        driver = open_website()
        input_title(driver, values["website"])
        click_search(driver)
        click_download(driver)
        close_website(driver)


main()
