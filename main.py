import time
from selenium import webdriver
import PySimpleGUI as sg
import os


def initialization():
    sg.SetOptions(text_justification="center", font=("Noto Sans", 18))
    sg.theme("Dark")

    layout = [[sg.Text("Status"), sg.Text("DOI Not Provided", key="status", text_color="orange")],
              [sg.Text("Please input doi / website of the paper you want to download: ")],
              [sg.Input(key="website")],
              [sg.Text("Please select the path for file downloading: ")],
              [sg.FolderBrowse(), sg.Input(key="path")],
              [sg.Button("OK"), sg.Button("Close"), sg.Stretch(),
               sg.T("GitHub", text_color="yellow",
                    enable_events=True, key="about", tooltip="Click to visit my GitHub page!")]]

    window = sg.Window("EZ-PaperDownloader v4.0.0", layout)
    return window


def window_operation(window):
    while True:
        event, values = window.read()
        if event in (None, "Close"):
            exit()
        if event == "OK":
            window["status"].update("Downloading, please wait for 5 seconds...", text_color="green")
            window.refresh()
            break
        if event == "about":
            url = "https://github.com/EZ-HKU"
            driver = webdriver.Chrome()
            driver.get(url)

    return values


def open_website(window):
    path = window["path"].get()
    os.chdir(path)
    op = webdriver.ChromeOptions()

    op.add_argument('--headless')
    op.add_experimental_option('excludeSwitches', ['enable-automation'])
    current_directory = os.path.dirname(os.path.abspath(__file__))
    prefs = {'--profile.default_content_settings.popups': 0,
             '--download.default_directory': current_directory}
    op.add_experimental_option('prefs', prefs)

    url = 'https://sci-hub.se/'
    driver = webdriver.Chrome(options=op)
    try:
        driver.get(url)
    except:
        sg.Popup("Poor Connection!")
        window.close()
        return main()
    return driver


def input_title(driver, title):
    try:
        in_put = driver.find_element("id", "request")
        in_put.send_keys(title)
    except:
        sg.Popup("OH,no! You are caught as a bot! Please try again later")
        exit()


def click_search(driver):
    search = driver.find_element("xpath", "//button[@type='submit']")
    search.click()


def click_download(driver):
    try:
        download = driver.find_element("xpath", "//button[@onclick]")
        download.click()
        time.sleep(3)
        sg.Popup("Download successfully, please check your \"download!\" folder!")
    except:
        sg.Popup("The paper does not exist!")


def close_website(driver, window):
    driver.close()
    window.close()


def main():
    while True:
        window = initialization()
        values = window_operation(window)
        driver = open_website(window)
        input_title(driver, values["website"])
        click_search(driver)
        click_download(driver)
        close_website(driver, window)


if __name__ == '__main__':
    main()
