import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from .Domains import Domains
from urllib import request
import math
from tqdm import tqdm


class CAPES():
    """ Classe de conexão e requisição ao site do Periódicos CAPES. """

    def __init__(self):
        self.articles = []
        self.count = 0
        self.domains = Domains()
        self.debug = True
        self.await_time = 30
        self.page = 1
        self.iframe = None
        self.profile = None
        self.browser = None
        self._await = None
        self.maxPage = -1
        


    def setProfile(self,_profile):
        self.profile = _profile
        
    def configureBrowser(self):
        #CHROME
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--ignore-certificate-errors')
        # options.add_argument('--proxy-server=socks5://localhost:5000')
        options.add_experimental_option("prefs", {
            "download.default_directory": self.profile['download-path'],
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,
        })
        self.browser = webdriver.Chrome(
            executable_path='./drivers/chromedriver.exe', 
            options=options
        )
        self._await = WebDriverWait(self.browser, self.await_time)

        #LOGIN NA CAPES
        url = 'http://www.periodicos.capes.gov.br/?option=com_plogin&ym=3&pds_handle=&calling_system=primo&institute=CAPES&targetUrl=http://www.periodicos.capes.gov.br&Itemid=155&pagina=CAFe'

        self.browser.get(self._get_url())

        self._await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'body > div.layout > footer > div.container.container-menus > div.row-fluid > div > div > div.modal-footer > button'))).click()

        self._await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#portal-siteactions > li:nth-child(1) > a'))).click()

        n_URL = ''
        select = self.browser.find_element_by_css_selector('#listaInstituicoesCafe')
        for option in select.find_elements_by_tag_name('option'):
            if option.get_attribute('text') == self.profile['institute']:
                n_URL = option.get_attribute('value').replace('#', '.')

        self.browser.get(n_URL)

        institutes = {
            'UFES - UNIVERSIDADE FEDERAL DO ESPÍRITO SANTO': self.loginUFES,
            'IFES - INSTITUTO FEDERAL DO ESPÍRITO SANTO' : self.loginIFES
        }

        if self.profile['institute'] in institutes:
            institutes[self.profile['institute']]()
        else:
            print('Instituto não cadastrado!')
            self.browser.quit()
            exit(0)

    def loginUFES(self):
        try:
            self.browser.find_element_by_css_selector(
                '#username').send_keys(self.profile['username'])
            self.browser.find_element_by_css_selector(
                '#password').send_keys(self.profile['password'])

            self.browser.find_element_by_css_selector('#login-main-content > div.loginMainContentLoginBox.clearfix > form > button').click()
            self._await.until(ec.element_to_be_clickable((By.CSS_SELECTOR, '#attribute-release-main-content > div.attributeReleaseMainContent.clearfix > div:nth-child(2) > div.button > ul > li:nth-child(2) > button'))).click()
            time.sleep(1)
        except Exception as err:
            print('Erro ao fazer login na UFES!')
            self.browser.quit()
            exit(1)

    def loginIFES(self):
        try:
            self.browser.find_element_by_css_selector(
                '#username').send_keys(self.profile['username'])
            self.browser.find_element_by_css_selector(
                '#password').send_keys(self.profile['password'])
            self.browser.find_element_by_css_selector('#login-main-content > div.loginMainContentLoginBox.clearfix > form > button').click()
            self._await.until(ec.element_to_be_clickable((By.CSS_SELECTOR, '#attribute-release-main-content > div.attributeReleaseMainContent.clearfix > div:nth-child(2) > div.button > ul > li:nth-child(2) > button'))).click()
            time.sleep(1)
        except Exception as err:
            print('Erro ao fazer login no IFES!')
            self.browser.quit()
            exit(1)


    def search(self,_query):
        self.articles = []
        # FIREFOX
        # profile = webdriver.FirefoxProfile()
        # profile.set_preference( "network.proxy.type", 1 )
        # profile.set_preference( "network.proxy.socks", "localhost" )
        # profile.set_preference( "network.proxy.socks_port", 5000 )
        # profile.set_preference( "network.proxy.socks_remote_dns", True )
        # browser = webdriver.Firefox(
        #     executable_path='drivers/geckodriver',
        #     firefox_profile=profile
        # )
        
        # Colocar a query na barra de busca
        search_bar = self._await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#assunto > form > div > div:nth-child(1) > input[type=text]')))
        search_bar.clear()
        search_bar.send_keys(_query)
        search_bar.send_keys(Keys.ENTER)
        
        # Esperando o resultado da busca
        self.iframe = self._await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#metabusca')))
        self.browser.switch_to_frame(self.iframe)

        
        # Verificando a quantidade de resultados recuperados, caso seja 0 vai para a outra busca
        max_result = 0
        #TODO: FAZER ISSO DE MANEIRA ELEGANTE
        result_resp =self._await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#resultsNumbersTile > h1:nth-child(1)'))).text.split()
        n = result_resp[0]
        if n.isnumeric():
            max_result = int(n)
        else:
            n = result_resp[6].replace('.','')
            if n.isnumeric():
                max_result = int(n)
        if max_result == 0:
            print('Nenhum resultado encontrado!')
            return None

        print('Total de paǵinas encontradas: ',math.ceil(max_result/10))

        if self.profile['max-pages']:
            if self.profile['max-pages'] == -1:
                self.maxPage = math.ceil(max_result/10)
            elif self.profile['max-pages'] <  math.ceil(max_result/10):
                self.maxPage = self.profile['max-pages']
                print('Máximo de páginas que serão recuperadas: ',self.maxPage)
            
            else:
                self.maxPage = math.ceil(max_result/10)

        # Começo a pegar os resultados de cada página da busca
        for self.page in tqdm(range(0,self.maxPage)):
            self._get_pages(self.page)
            # if self.page == self.maxPage:
                # break

        self.browser.quit()
        return self.articles

    def _get_pages(self, count, page=1):
        url = self.browser.current_url
        next_page = None
        #Procuro se existe o botão de próxima página
        try:
            pages = self._await.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR,'#resultsNavNoId > a')))
            for i in range(0,len(pages)):
                if pages[i].get_attribute('title') == 'Ir para próxima página':
                    next_page = pages[i]
                    break
        except Exception as e:
            # print('Não foi encontrada mais paginas de resultados!')
            # print(e)
            pass

        # Tento pegar os resultados
        try:
            elements = self._await.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR,'#exlidResultsTable > tbody > tr')))
        except Exception as e:
            print("Sem resultados!")
            return None

        # Processando os resultados
        self._get_elements(elements)
        

        # Tento ir para próxima página caso tenha
        if next_page:
            try:
                next_page.click()
                return None
            except Exception as e:
                print('Erro ao seguir para a próxima página!')
                print(e)
                return None
        else:
            return None
    
    def _get_article_info(self, _element,_i):
        try:
            det =self._await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#exlidResult'+str(_i)+'-detailsTabLink')))
            det.click()
        except NoSuchElementException:
            print(e)
            print('Elemento não encontrado/renderizado!')
            # det =self._await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#exlidResult'+str(_i)+'-detailsTabLink')))
            # det.click()
        
        try:
            title =self._await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#exlidResult'+str(_i)+'-TabContent > div.EXLDetailsContent > ul > li:nth-child(2) > div'))).text
        except Exception as e:            
            return None
        try:
            authors = _element.find_element_by_css_selector('#Autor'+str(_i)+'').text.replace('Autor: ','')
        except Exception as e:
            authors = None
        try:
            abstract = _element.find_element_by_css_selector('#Descrição'+str(_i)+' > span').text
        except Exception as e:
            abstract = None
        try:
            link_paper = _element.find_element_by_css_selector('#exlidResult'+str(_i)+' > td.EXLSummary > div.EXLSummaryContainer > div > h2 > a').get_attribute('href')
        except Exception as e:
            link_paper = None
        try:
            keywords = _element.find_element_by_css_selector('#Assuntos'+str(_i)+'').text.replace('Assuntos: ','')
        except Exception as e:
            keywords = None
        try:
            year = _element.find_element_by_css_selector('#Publicado\ em'+str(_i)+'').text
        except Exception as e:
            year = None
        try:
            language = _element.find_element_by_css_selector('#Idioma'+str(_i)+'').text.replace('Idioma: ','')
        except Exception as e:
            language = None
        try:
            doi = _element.find_element_by_css_selector('#Identificador'+str(_i)+' > span').text
            aux =  doi.split(';')
            d = [a for a in aux]
            doi = {}
            for i in d:
                i = i.split(':')
                doi[i[0].replace(' ','')] = i[1].replace(' ','')
        except Exception as e:
            doi = None
        try:
            font = _element.find_element_by_css_selector('#Fonte'+str(_i)+' > span').text
        except Exception as e:
            font = None
        
        doc = {
            'title': title,
            'authors': authors,
            'abstract': abstract,
            'keywords': keywords,
            'language': language,
            'font' : font,            
            'link' : link_paper,
        }

        if doi:
            for i in doi:
                if i:
                    doc[i] = doi[i]
        return doc

    def _get_elements(self, elements):
        # Para cada resultado(elemento) pego os dados do artigo
        self.count += len(elements)
        for i in range(0,len(elements)):
            elem = elements[i]

            # Organizo os dados do artigo
            doc = self._get_article_info(elem,i)
            if doc:            
                self.articles.append(doc)


            # TODO: Remover o continue quando finalizar o download dos arquivos
            continue
            
            self.browser.execute_script('''window.open("about:blank", "_blank");''')
            self.browser.switch_to_window(self.browser.window_handles[-1])
            self.browser.get(doc['link'])

            paper_url =  self.browser.current_url
            new_domain = True
            for domain in self.domains.model_law:            
                if domain in paper_url:
                    paper_link = self.domains.model_law[domain](self.browser,self._await)
                    if paper_link:
                        doc['link'] = paper_link
                        # self.browser.switch_to.window(self.browser.window_handles[-1])
                        # browser.close()
                        self.browser.switch_to.window(self.browser.window_handles[-1])
                        doc['file'] = self.domains.get_file_download_manager(self.browser)
                        self.browser.close()
                        self.browser.switch_to.window(self.browser.window_handles[-1])
                        self.articles.append(doc)                        
                    else:
                        self.domains.erro_log(paper_url)
                    new_domain = False
            self.browser.close()
            self.browser.switch_to_window(self.browser.window_handles[0])
            self.browser.switch_to_frame(self.iframe)

    def _get_url(self):
        return 'http://www.periodicos.capes.gov.br/?option=com_plogin&ym=3&pds_handle=&calling_system=primo&institute=CAPES&targetUrl=http://www.periodicos.capes.gov.br&Itemid=155&pagina=CAFe'

