import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains

import socks
import socket
from urllib import request
import math
from tqdm import tqdm
import json
from libs.Domains import Domains

print('Testando os dominios!!!')
#CHROME
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--proxy-server=socks5://localhost:5000')
options.add_experimental_option("prefs", {
    "download.default_directory": "/home/manogueira/Downloads/Articles/",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True,
})
browser = webdriver.Chrome(
    executable_path='drivers/chromedriver', 
    options=options
)

_await = WebDriverWait(browser, 5)

data = {}
with open('/dados/resultados-buscas/Lama-de-beneficiamento-de-rochas-ornamentais.json') as f:
    data = json.load(f)


domains = Domains()

bl = ['sciencedirect',
        'journals-sagepub-com',
        'openurl-ebscohost',
        'onlinelibrary-wiley',
        'www-emerald',
        'doaj.org']
for x,i in enumerate(data):
    ok = False
    link = i['link']
    browser.get(link)
    _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'body')))
    paper_url =  browser.current_url
    print(i['title'])
    print(paper_url)
    for domain in domains.model_law:            
        if domain in paper_url:
            print(i['title'])
            print(domain)
            if not domain in bl:
                ok = True
            # TODO: RESOLVER PROLEMA INTERMITENTE COM O ACESSO AOS PDFS
            paper_link = domains.model_law[domain](browser,_await)
            if paper_link:
                print(paper_link)
                browser.switch_to.window(browser.window_handles[-1])
                _file = domains.get_file_download_manager(browser)
                browser.switch_to.window(browser.window_handles[0])
                print(_file)
                break
                # print(doc)
            
    print('--------------------')
    if ok:
        print('WAIT!')
        input()
browser.quit()
exit()



url = 'http://www.periodicos.capes.gov.br/?option=com_plogin&ym=3&pds_handle=&calling_system=primo&institute=CAPES&targetUrl=http://www.periodicos.capes.gov.br&Itemid=155&pagina=CAFe'
await_time = 5
_await = WebDriverWait(browser, await_time)


browser.execute_script('''window.open("about:blank", "_blank");''')

browser.switch_to.window(browser.window_handles[-1])
browser.get('chrome://downloads/')
input()
browser.quit()
exit(1)


browser.get(url)

