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

    window = sg.Window("EZ-PaperDownloader v4.2.0", layout)
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

    download_location = os.path.abspath(path)
 
    prefs = {'download.default_directory': download_location,
             'download.prompt_for_download': False,
             'download.directory_upgrade': True,
             'safebrowsing.enabled': True,
             'safebrowsing.disable_download_protection': True}

    op.add_experimental_option('prefs', prefs)

    # op.add_argument('--headless')
    op.add_argument('--disable-gpu')

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
    while (True):
        time.sleep(1)
        try:
            in_put = driver.find_element("id", "request")
            in_put.send_keys(title)
            break
        except:
            if sg.PopupYesNo("Please Finish the Captcha!") == "No":
                driver.close()
                exit()



def click_search(driver):
    search = driver.find_element("xpath", "//button[@type='submit']")
    search.click()


def click_download(driver, path):
    try:
        download = driver.find_element("xpath", "//button[@onclick]")
        download.click()

        # check if the file exists, "I only know if the file's suffix is .tmp, means not exist"
        while True:
            count = 0
            files = os.listdir(path)
            for file in files:
                if file.endswith(".tmp") or file.endswith(".crdownload"):
                    count += 1

            if count == 0:
                sg.Popup(f"Download successfully, please check your {path} folder!")
                break

            elif count != 1:
                time.sleep(1)

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
        click_download(driver, values["path"])
        close_website(driver, window)


if __name__ == '__main__':
    main()
