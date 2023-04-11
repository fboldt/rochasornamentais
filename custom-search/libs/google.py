import certifi
import requests
import os
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
from tika import parser
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from requests.exceptions import ConnectionError, ChunkedEncodingError, StreamConsumedError, SSLError, TooManyRedirects
from urllib3.exceptions import MaxRetryError
from .__errors__ import __errors__
from .database.database import Connection

class Google():
    """ Classe de conexão e requisição ao site do Google Scholar. """

    _parser = BibTexParser()
    _parser.customization = convert_to_unicode
    articles = []
    page = 0

    def search(self, query, max_page = 2):
        """ Função de busca simulando um browser a partir do `Selenium`.\n
        Argumento:\n
            str - palavras chaves da busca.
            int - námero de páginas a serem percorridas.\n
        Retorno:\n
            list - lista do artigos coletados (título/link). """
        print('\nInit search on Google Scholar')

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
            # firefox_options=options
        )

        _await = WebDriverWait(browser, 180)
        _id = Connection().get_last_id_inserted('article')['id']

        while self.page <= max_page:
            browser.get(self._get_url(query, self.page))
            try:
                _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#gs_captcha_ccl')))
                sleep(2400)
                self.search(query, max_page)
            except:
                pass
            print('Search in ', self._get_url(query, self.page))
            sleep(60)
            
            elements = _await.until(ec.presence_of_all_elements_located((By.XPATH, '//*[@id="gs_res_ccl_mid"]/div')))

            title = None
            link = None
            author = None
            year = None
            abstract = None
            fulltext = None
            count = 1
            for elem in elements:
                try:
                    title = elem.find_element_by_css_selector('div:nth-child(' + str(count) + ') > div.gs_ri > h3')
                    link = elem.find_element_by_css_selector('div:nth-child(' + str(count) + ') > div.gs_ggs.gs_fl > div > div > a')
                    
                    if 'PDF' in link.text:
                        print('\nGetting PDF infos')
                        title = title.text
                        link = link.get_attribute('href')
                        print({ 'title': title, 'link': link })
                        
                        try:
                            _await.until(ec.visibility_of_element_located(
                                (By.CSS_SELECTOR, '#gs_res_ccl_mid > div:nth-child(' + str(count) + ') > div.gs_ri > div.gs_fl > a.gs_or_cit.gs_nph'))).click()
                            sleep(11)

                            _await.until(ec.visibility_of_element_located(
                                (By.CSS_SELECTOR, 'a.gs_citi'))).send_keys(Keys.CONTROL, Keys.ENTER)
                            sleep(5)
                           
                            main_window = browser.current_window_handle
                            windows = browser.window_handles
                            browser.switch_to.window(windows[1])
                            sleep(10)
                            
                            _bibtex = _await.until(ec.visibility_of_element_located((By.TAG_NAME, 'pre'))).text
                            sleep(20)
                            
                            browser.close()
                            sleep(5)
                            browser.switch_to.window(main_window)
                            sleep(5)
                            _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#gs_cit-x'))).click()
                            sleep(11)

                            author, year = self._extract_infos(_bibtex)
                            filename = self._download(link)
                            fulltext = self._extract_fulltext(filename)

                            _id += 1
                            print(_id)

                            self.articles.append({
                                'id': _id,
                                'query': query,
                                'title': title,
                                'link': link,
                                'authors': author,
                                'year': year,
                                'abstract': abstract,
                                'fulldoc': fulltext})

                            print('\nArticle inserted.\n')
                        except Exception as exc:
                            __errors__(str(exc))
                            pass

                except Exception as exc:
                    print('--- Error find element ', exc)
                    __errors__(str(exc))
                    pass
                
                count += 1

            sleep(35)
            self.page += 1

        browser.quit()

        return self.articles

    def _extract_infos(self, bibtex):
        print('\nExtract BibTex: ', end='')
        _bibtex = bibtexparser.loads(bibtex, parser=self._parser)
        dic = _bibtex.get_entry_dict() 
        author = ''
        year = ''

        for i in dic:
            author = dic[i]['author']
            year = dic[i]['year']
        
        print(author, year)
        return author, year

    def _extract_fulltext(self, filename):
        print('\nExtract Full Text', filename)
        
        try:
            parsed = parser.from_file(filename)
            pdf_file = parsed["content"]

            if pdf_file:
                aux = pdf_file.split('\n')
                _file = ''
                for x in aux:
                    if x:
                        _file += x

            return _file
        except Exception as exc:
            __errors__('Error extract text ' + str(exc))
            

    def _get_url(self, query, page):
        """ Função de construção do link completo.\n
        Está se buscando também por patentes.\n
        Não se está sendo considerado Citações.\n
        Argumento:\n
            str - palavras chaves da busca.
            int - número da página.\n
        Retorno:\n
            str - link completo da busca. """
        return 'https://scholar.google.com.br/scholar?q=' + '+'.join(query.split()) + '&as_sdt=0,5&hl=pt-BR&as_vis=1&ie=utf-8&oe=utf-8&start=' + str(page) + '0'

    def _download(self, link):
        ''' Metodo de download do artigo.\n
        Argumento:\n
            str - link do arquivo PDF. '''
        
        print('\nDownloading PDF')

        if not os.path.exists('download'):
            os.mkdir('download')

        try:
            res = requests.get(link, stream=True, verify='./cacert.pem')
            print('Getting file PDF')
        except StreamConsumedError as err_stream:
            __errors__('StreamConsumedError: ' + str(err_stream))
        except MaxRetryError as err_max:
            __errors__('MaxRetryError: ' + str(err_max))
        except SSLError as err_ssl:
            __errors__('SSLError: ' + str(err_ssl))
        except TooManyRedirects as err_tmr:
            __errors__('TooManyRedirects: ' + str(err_tmr))
        except Exception as exc:
            __errors__(exc)

        url_parse = link.split('/')
        name_file = url_parse[-1].split('.')
        name = './download/' + name_file[0] + '.pdf'

        if not os.path.isfile(name):
            try:
                print('Building file')
                with open(name, "wb") as py_pdf:
                    try:
                        for chunk in res.iter_content(chunk_size=1024):
                            if chunk: 
                                py_pdf.write(chunk)
                        print('File downloaded.\n')
                    except ChunkedEncodingError as err:
                        __errors__('ChunkedEncodingError: ' + str(err)) 
            except:
                __errors__('Error open file in: ' + str(link))

        return name
        
''' Modulo para busca de artigos no Google Scholar usando requests/urllib. '''
"""
class GoogleIt:
    ''' O modulo depende de uma chamada assincrona, uma vez que se trata de uma requisicao web.\n
    Argumento: palavra chave da busca. <`str`>.\n
    Exemplo:

        async def main():
            await GoogleIt('search it').start()
    
    '''

    import os
    import requests_async
    import requests
    import parslepy
    import csv
    from time import sleep
    from random import randint
    from datetime import datetime
    from requests.exceptions import ConnectionError, ChunkedEncodingError, StreamConsumedError, SSLError, TooManyRedirects
    from urllib3.exceptions import MaxRetryError
    import certifi

    def __init__(self, search):
        ''' Contrutor da classe.
        
        self._header 
        - cabecalho da requisicao web.
        
        self._rules 
        - url da requisicao.
        - container `dict` que recebera as informacoes do request.
        
        Argumento: self.search - a `string` de busca. '''

        self._header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,la;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self._rules = {
            'scholar': {
                'url': 'https://scholar.google.com.br/scholar?q=',
                'container': {
                    'wrapper([data-did])': [{
                        'content(h3.gs_rt)': [{
                            "span": "span",
                            "title": "a",
                            "link": "a/@href"
                        }],
                        "another(div.gs_or_ggsm)": [{
                            "link": "a/@href"
                        }]
                    }]
                }
            }
        }

        self.search = search

    def __errors__(self, log):
        ''' Metodo de escrita dos eventuais erros em um arquivo de log.\n
        Argumento: 
        - log do erro `string`. '''

        with open('./errors.txt', 'a', encoding='utf-8') as error:
            try:
                print(log)
                error.write('[' + str(datetime.now()) + '] - ' + log + '\n')
            except UnicodeEncodeError as err:
                print(err)
            except:
                print('Another error.')
            finally:
                error.close()

    def _download(self, link):
        ''' Metodo de download do artigo.\n
        Argumento: link `string` do arquivo PDF. '''

        try:
            res = requests.get(link, stream=True, verify='./cacert.pem')
            print('Getting file PDF')
        except StreamConsumedError as err_stream:
            self.__errors__('StreamConsumedError: ' + str(err_stream))
        except MaxRetryError as err_max:
            self.__errors__('MaxRetryError: ' + str(err_max))
        except SSLError as err_ssl:
            self.__errors__('SSLError: ' + str(err_ssl))
        except TooManyRedirects as err_tmr:
            self.__errors__('TooManyRedirects: ' + str(err_ssl))
        except:
            self.__errors__('Other error in download method')

        url_parse = self._parser(link, '/')
        name_file = self._parser(url_parse[-1], '.')
        name = './uploads/' + name_file[0] + '.pdf'

        if not os.path.isfile(name):
            try:
                with open(name, "wb") as py_pdf:
                    try:
                        for chunk in res.iter_content(chunk_size=1024):
                            if chunk: py_pdf.write(chunk)
                            print('Building file with chunks')
                    except ChunkedEncodingError as err:
                        self.__errors__('ChunkedEncodingError: ' + str(err)) 
            except:
                self.__errors__('Error open file in: ' + link)
        else:
            print('File downloaded.')

    def _parser(self, word, separator=' '):
        ''' Funcao separador de `string` em `list`. \n
        Argumento: \n
        - palavra/frase a ser separada `string`.
        - separador, `default=' '` 
            
        Exemplo: 
            
        >>> _parser('frase de teste')

        Retorno: 
        list >>> ['frase', 'de', 'teste'] '''

        return word.split(separator)

    def _save_files(self, extracted):
        ''' Funcao que salva o arquivo.\n
        Cria uma pasta na raiz da requisicao do modulo `uploads`.\n
        Argumento: \n
        - o objeto que foi extraido do HTML da requisicao `extracted`.

        Retorno: \n
        - `True` caso tenha alguma informacao no objeto recebido.
        - `False` caso o embrulho esteja vazio. '''

        if not os.path.exists('uploads'):
            os.mkdir('uploads')

        if extracted['wrapper'] != []: 
            for item in extracted['wrapper']:
                if item['another'] != []:
                    print('Download file on Google Scholar: ', item['another'][0]['link'])
                    self._download(item['another'][0]['link'])
                    print('Await 1 minute to the next file extracted.')
                    sleep(60)
            return True

        return False
        
    def _save_csv(self, content):
        ''' Metodo para escrita no arquivo CSV com os titulos e os links dos artigos.\n

        Argumento: \n
        - conteudo extraido, parte do objeto que contem as informacoes necessarias. '''

        with open('./articles.csv', 'a', newline='') as fl:
            try:
                writer = csv.writer(fl)
                writer.writerow([
                    content['content'][0]['title'], 
                    content['another'][0]['link']
                ])
                print('CSV wrote.')
                fl.close()
            except:
                self.__errors__('Error write articles.csv.')
    
    def _file_verifying(self, content):
        ''' Método que verifica se o arquivo já está contido no csv. \n

        Argumento: \n 
        - conteudo extraido, parte do objeto que contem as informacoes necessarias.
        
        Retorno: \n
        - `True` caso o arquivo ja esteja no CSV.
        - `False` caso ainda nao esteja escrito no CSV. '''

        with open ('./articles.csv', newline='') as csvfile:
            csvreader = csv.DictReader(csvfile, fieldnames=["Title", "Link"], delimiter=",")
            for row in csvreader:
                if row["Link"] == content['another'][0]['link']:
                    return True
            return False

    async def _get_request(self, url):
        ''' Funcao para requisicao. \n
        Argumento: \n
        - `url` da requisicao.

        Retorno: \n 
        - `Session` objeto, contendo o texto HTML, Status Code, etc.
        - `False` caso haja algum erro. '''

        try:
            session = requests_async.Session()
            result = await session.get(url, headers=self._header, verify='./cacert.pem')
            return result
        except ConnectionError as err:
            self.__errors__('ConnectionError: ' + str(err)) 
        except MaxRetryError as err_max:
            self.__errors__('MaxRetryError: ' + str(err_max))
        except SSLError as err_ssl:
            self.__errors__('SSLError: ' + str(err_ssl))
        except TooManyRedirects as err_tmr:
            self.__errors__('TooManyRedirects: ' + str(err_ssl))
        except:
            self.__errors__('Other error in download method')
        return False
    
    async def _response(self, url_search):
        ''' Funcao de requisicao da pagina. \n

        Argumento: \n
        - `url` da requisicao.
        
        Retorno: \n
        - `Session` objeto, contendo o texto HTML, Status Code, etc.
        - `None` caso haja algum erro. '''

        print('Request init:', url_search)
        result = await self._get_request(url_search)
        if result == False: return None

        while result.status_code == 429:
            print('Status Code 429\nToo Many Requests\nAwait some minutes to next request')
            self.__errors__('Status Code: ' + str(result.status_code) + '\n' + '<Too Many Requests>')

            seconds = randint(180, 360)
            print('Await', seconds, 'seconds to try again')
            sleep(seconds)
            
            print('Request init:', url_search)
            result = await self._get_request(url_search)
            if result == False: return None
        
        return result
    
    async def start(self, num_page=3):
        ''' Metodo que inicia a busca.\n
        Argumento: \n
        - numero de paginas a serem buscadas, `default=3` '''
        
        page = 0
        while page < num_page:
            print('Start search')

            # escreve a url completa de busca
            url = self._rules['scholar']['url']
            query = '+'.join(self._parser(self.search))
            url_search = url + query + '&as_sdt=0,5&hl=pt-BR&as_vis=1&ie=utf-8&oe=utf-8&start=' + str(page) + '0'

            result = await self._response(url_search)

            # receber a requisicao e trata para transformar em um objeto (dict)
            parse = parslepy.Parselet(self._rules['scholar']['container'])
            extracted = parse.parse_fromstring(result.text)

            if extracted['wrapper'] == []:
                self.__errors__('Extracted empty: ' + str(extracted))
                return None

            if self._save_files(extracted): 
                print('Files saved')
            else:
                print("There's no files here.")
                return None

            for content in extracted['wrapper']:
                if content['another'] != []:
                    if self._file_verifying == False:
                        print('Wrinting CSV.')
                        self._save_csv(content)

            seconds = randint(180, 360)
            print('Await', seconds, 'seconds to next request')
            sleep(seconds)

            page += 1
"""
