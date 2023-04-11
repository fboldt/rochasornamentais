import os
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

if not os.path.exists('download'):
    os.makedirs('download')


def initialize_browser():
    url = 'https://www.periodicos.capes.gov.br/?option=com_plogin&ym=3&pds_handle=&calling_system=primo&institute=CAPES&targetUrl=http://www.periodicos.capes.gov.br&Itemid=155&pagina=CAFe'

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--ignore-certificate-errors")
    options.add_experimental_option(
        "prefs", {
            "download.default_directory": r"./download",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })

    browser = webdriver.Chrome(
        executable_path=r'./driver/chromedriver.exe' if os.name == 'nt' else r'./driver/chromedriver', options=options)

    _await = WebDriverWait(browser, 30)
    browser.get(url)

    return browser, _await
