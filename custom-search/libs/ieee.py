from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class IEEE:

    def search(self, query):
        print('Init search on IEEE Xplore\n')

        # options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        # browser = webdriver.Chrome(executable_path='./lbro/enginesearch/drivers/chromedriver.exe',chrome_options=options)

        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        browser = webdriver.Firefox(
            executable_path='./lbro/enginesearch/drivers/geckodriver',
            # firefox_options=options
        )
            
        _await = WebDriverWait(browser, 180)

        url = self._get_url(query)
        print('Getting elements', url)
        browser.get(url)
        sleep(35)

        elements = _await.until(ec.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, '#xplMainContent > div.ng-SearchResults.row > div.main-section')))

        for elem in elements:
            print(elem.text())

        sleep(15)
        browser.quit()

    def _get_url(self, query):
        return 'https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText=' + '+'.join(query.split())

IEEE().search('python engine')
