import time
from selenium import webdriver
from selenium.webdriver.common.by import By
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
             'safebrowsing.disable_download_protection': True,
             "plugins.always_open_pdf_externally": True
             }

    op.add_experimental_option('prefs', prefs)

    op.add_argument('--headless')
    op.add_experimental_option('excludeSwitches', ['enable-automation'])
    op.add_argument('--disable-gpu')

    url = 'https://sci-hub.hkvisa.net/'
    driver = webdriver.Chrome(options=op)
    try:
        driver.get(url)
    except:
        sg.Popup("Poor Connection!")
        window.close()
        return main()
    return driver, op


def input_title(driver, title):
    while (True):
        time.sleep(1)
        try:
            in_put = driver.find_element("name", "request")
            in_put.send_keys(title)
            break
        except:
            if sg.PopupYesNo("Please Finish the Captcha!") == "No":
                driver.close()
                exit()


def click_search(driver):
    search = driver.find_element("id", "open")
    search.click()


def get_doi(driver):
    citation = driver.find_element("id", "citation")
    citation = citation.text
    doi_beg = citation.find("doi")
    doi_end = citation.find("&nbsp")
    doi = citation[doi_beg + 4:doi_end]
    # print(doi)
    return doi


# 根据DOI打开新网页
def click_download(doi, path, window, op):
    driver = webdriver.Chrome(options=op)
    url = "https://sci.bban.top//pdf//" + doi + ".pdf"
    try:
        driver.get(url)
    except:
        sg.Popup("no such page according to DOI")
        window.close()
        return main()

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

    # try:
    # time.sleep(2)
    # # click download button in iframe
    # driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, 'body > embed'))
    # # driver.switch_to.frame(driver.find_element('name', '7DCBA13E53623FF31E9F584816C7BEF8'))
    # print("switched")
    # download = driver.find_element("id", "download")
    # print("find")
    # print(download)
    # download.click()

    # check if the file exists, "I only know if the file's suffix is .tmp, means not exist"
    # while True:
    #     count = 0
    #     files = os.listdir(path)
    #     for file in files:
    #         if file.endswith(".tmp") or file.endswith(".crdownload"):
    #             count += 1
    #
    #     if count == 0:
    #         sg.Popup(f"Download successfully, please check your {path} folder!")
    #         break
    #
    #     elif count != 1:
    #         time.sleep(1)

    # except:
    #     sg.Popup("The paper does not exist!")

    return driver


def close_website(driver, window):
    driver.close()
    window.close()


def main():
    while True:
        window = initialization()
        values = window_operation(window)
        driver, op = open_website(window)
        input_title(driver, values["website"])
        try:
            click_search(driver)
        except:
            continue
        doi = get_doi(driver)
        driver.close()
        driver = click_download(doi, values["path"], window, op)
        close_website(driver, window)


if __name__ == '__main__':
    main()
