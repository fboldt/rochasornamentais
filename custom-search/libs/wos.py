from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class WOS():
    """ Classe de conexão e requisição ao site do Google Scholar. """

    def __init__(self):
        self.articles = []
        self.count = 1

    def search(self, query):
        """ Função de busca simulando um browser a partir do `Selenium`.\n
        Argumento:\n
            str - palavras chaves da busca.
        Retorno:\n
            list - lista do artigos coletados (título/link). """
        print('Init search on Web of Science\n')

        # options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        # browser = webdriver.Chrome(
        #   executable_path='./drivers/chromedriver', 
        #   chrome_options=options
        # )

        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        browser = webdriver.Firefox(
            executable_path='./drivers/geckodriver', 
            firefox_options=options
        )

        _await = WebDriverWait(browser, 180)

        browser.get(self._get_url())
        print(self._get_url())
        sleep(120)

        input_text = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'input.focusinput.search-criteria-input')))
        input_text.send_keys(query)
        input_text.send_keys(Keys.ENTER)

        count = 1

        self._get_pages(browser, _await, count)

        sleep(60)

        browser.quit()
        
        return self.articles

    def _get_pages(self, browser, _await, count, page=2):
        """ Método para busca dos artigos.\n
        Argumento:\n
            str - url da requisição.
            int - número da página. """
        url = browser.current_url
        print('\nGetting page WOS\n', url)
        
        elements = _await.until(ec.visibility_of_all_elements_located((By.CSS_SELECTOR,'#records_chunks > div.search-results > div.search-results-item')))

        last_page = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#pageCount\.bottom')))

        self._get_elements(browser, _await, elements)
        
        if page <= int(last_page.text):
            page += 1
            _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#summary_navigation > nav > table > tbody > tr > td:nth-child(3) > a'))).click()
            sleep(15)
            self._get_pages(browser, _await, page)

    def _get_elements(self, browser, _await, elements):
        print('\nGetting elements\n')
        title = None
        authors = None
        year = None
        abstract = None
        url = None
        for elem in elements:
            print('\nCount element ', self.count)

            _result_data = '#RECORD_' + str(self.count) + ' > div.search-results-data'
            if _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR, _result_data))).text != '':
                _css_selector = '#RECORD_' + str(self.count) + ' > div.search-results-content > div:nth-child(1)'
                title = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR, _css_selector))).text

                try:
                    authors = _await.until(ec.visibility_of_element_located(
                        (By.CSS_SELECTOR, '#RECORD_' + str(self.count) + ' > div.search-results-content > div:nth-child(2)'))).text 
                except Exception as exc:
                    authors = _await.until(ec.visibility_of_element_located(
                        (By.CSS_SELECTOR, '#RECORD_' + str(self.count) + ' > div.search-results-content > div:nth-child(3)'))).text
                
                year = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR, '.data_bold'))).text

                _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#abstract-text' + str(self.count)))).click()
                sleep(5)
                abstract = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#ViewAbstract_TextArea' + str(self.count)))).text

                _css_selector = '#links_openurl_' + str(self.count) + ' > a'
                button = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR, _css_selector)))
                button.click()

                sleep(30)

                windows = browser.window_handles
                sleep(10)
                browser.switch_to.window(windows[1])

                sleep(15)
                url = browser.current_url

                # title, link, authors, year, abstract
                self.articles.append({
                    'title': title, 
                    'link': url, 
                    'authors': authors, 
                    'year': year, 
                    'abstract': abstract,
                    'fulldoc': ''
                })
                print(title)

                browser.close()

                browser.switch_to.window(windows[0])

            '''
            else: 
                _patent = _await.until(ec.visibility_of_element_located(
                    (By.CSS_SELECTOR, '#RECORD_' + str(self.count) + ' > div.search-results-content > div:nth-child(1) > div > a')))
                title = _patent.text
                link = _patent.get_attribute('href')
                number = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#RECORD_' + str(self.count) + ' > div.search-results-content > div:nth-child(2) > span.data_bold'))).text
                assignee = _await.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="RECORD_' + str(self.count) + '"]/div[3]/div[3]'))).text
                inventors = _await.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="RECORD_' + str(self.count) + '"]/div[3]/div[4]'))).text

                # title, link, number, assignee, inventors
                self.articles.append({
                    'title': title, 
                    'link': link, 
                    'number': number, 
                    'assignee': assignee, 
                    'inventors': inventors
                })
                print(title)
            '''
            self.count += 1

    def _get_url(self):
        """ Função de construção do link completo.\n
        Argumento:\n
            int - número da página. 
        Retorno:\n
            str - link completo da busca. """
        return 'http://apps-webofknowledge.ez120.periodicos.capes.gov.br/WOS_GeneralSearch_input.do?product=UA&search_mode=GeneralSearch'
