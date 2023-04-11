import json
from time import sleep
from random import choice
from elsapy.elsclient import ElsClient
from elsapy.elssearch import ElsSearch
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from requests import HTTPError
from .__errors__ import __errors__
from .database.database import Connection

class Scopus:
    """ Classe de busca na API do Scopus.\n
    Para inicialização do sistema é necessário uma chave de acesso a API, obtida em https://dev.elsevier.com/apikey/manage. """

    _keys = [
        '36b9a70ddf4a6b5c94727f0bd78c119c', 
        'f01d995a362758fab2b17583077eb860', 
        'ae3abd35fdbb65c2ae7b69c079c2e9e7'
    ]
    
    def __init__(self):
        self.articles = []
        self.query = ''
    
    def search(self, query):
        """ Função de busca no Scopus a partir de sua API.\n
        Argumento:\n
            str - palavras chaves da busca.
        Retorno:\n
            list - lista dos resultados obtidos (tÍtulo/link). """
        print('\nInit search on Scopus API')
        self.query = query
        try:
            self.client = ElsClient(choice(self._keys))
            _search = ElsSearch(self.query, 'sciencedirect')
            _search.execute(self.client, get_all=True)
            print("Found", len(_search.results), "results with", self.query, '\n')
        except HTTPError as err:
            self.search(self.query)
        except Exception as exc:
            __errors__('Error search Scopus. <function search()> ' + str(exc))
            return False
        return self._get_result()
    
    def _get_result(self):
        """ Função para construção a lista de artigos extraÍdos.\n
        Retorno:\n
            list - lista dos resultados obtidos. """
        
        _id = Connection().get_last_id_inserted('article')['id']    
        count = 1
        try:
            with open('./dump.json', 'r', encoding='utf-8') as fl:
                obj = json.load(fl)
            for i in obj:
                print(count, ' of ', len(obj))
                authors = None
                abstract = None
                fulltext = None
                try:
                    authors = self._get_authors(i['authors'])
                    abstract, fulltext = self._get_text(i['link'][1]['@href'])
                    _id += 1
                    self.articles.append({
                        'id': _id,
                        'query': self.query,
                        'title': i['dc:title'], 
                        'link': i['link'][1]['@href'], 
                        'authors': authors, 
                        'year': i['prism:coverDate'], 
                        'abstract': abstract,
                        'fulldoc': fulltext})
                    print('Article inserted.\n')
                    count += 1
                except Exception as e:
                    __errors__('<for - function _get_result()> ' + str(e))
                    continue
        except Exception as exc:
            __errors__('Error search Scopus. <function _get_result()> ' + str(exc))
            return False

        return self.articles

    def _get_text(self, url):
        # options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        # browser = webdriver.Chrome(
        #   executable_path='./lbro/enginesearch/drivers/chromedriver',
        #   chrome_options=options
        # )

        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        browser = webdriver.Firefox(
            executable_path='./lbro/enginesearch/drivers/geckodriver',
            firefox_options=options
        )
        
        _await = WebDriverWait(browser, 30)
        browser.get(url)
        print('Getting abstract ', url, '\n')
       
        _abstract = None
        _fulltext = None

        try:
            _abstract = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR, '.abstract.author > div'))).text
        except Exception as exc:
            __errors__('Error get Abstract.\n<function _get_text()> ' + str(exc))

        try:
            _fulltext = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#body'))).text
        except Exception as exc:
            __errors__('Error get FullText.\n<function _get_text()> ' + str(exc))

        browser.quit()
        return _abstract, _fulltext

    def _get_authors(self, authors):
        try:
            if type(authors['author']) == list:
                a = [ author['$'] for i in authors for author in authors[i] ]
                return '; '.join(a)
            return authors['author']
        except Exception as exc:
            __errors__('Error get authors <function _get_authors> ' + str(exc))
