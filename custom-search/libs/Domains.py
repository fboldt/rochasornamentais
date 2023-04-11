from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys


class Domains():
    """ Classe dos domínios dos artigos buscados."""

    def __init__(self):
        self.blacklist = [
            'openurl-ebscohost',
            'jlis.glis.ntnu.edu.tw',
            'scielo',
            'sp-lyellcollection',
            'mdpi',
            'oaj.fupress.net/index.php/techne',
            'ethnobiomed.biomedcentral.com.ez120.periodicos.capes.gov.br',
            'academic-eb-britannica',
            'www.dovepress.com/international-journal-of-wine-research-journal'
        ]
        self.model_law = {
            'sciencedirect' : self._sciencedirect,
            # 'projecteuclid' : self._projecteuclid,
            # 'web-a-ebscohost' : self._web_a_ebscohost,
            # 'web-b-ebscohost' : self._web_b_ebscohost,
            'link-springer-com' : self._link_springer_com,
            'journals-sagepub-com':self._journals_sagepub_com,
            'academic-oup-com':self._academic_oup_com,
            # 'www-cambridge':self._www_cambridge,
            # 'go-gale':self._go_gale,
            # 'pubs-rsc-org':self._pubs_rsc_org,
            # 'www-ncbi-nlm-nih-gov':self._www_ncbi_nlm_nih_gov,
            # 'www-emerald':self._www_emerald,
            # 'www-tandfonline':self._www_tandfonline,
            # 'muse-jhu-edu': self._muse_jhu_edu,
            # 'www-annualreviews-org': self._www_annualreviews_org,
            # 'oecd-ilibrary-org':self._oecd_ilibrary_org,
            # 'doaj.org':self._doaj,
            'openurl-ebscohost':self._openurl_ebscohost,
            'onlinelibrary-wiley': self._onlinelibrary_wiley,
            'scielo.br': self._scielo
        }

    def get_file_download_manager(self,_browser):
        _browser.execute_script('''window.open("about:blank", "_blank");''')
        _browser.switch_to_window(_browser.window_handles[-1])
        _browser.get('chrome://downloads/')
        progress = _browser.execute_script('''
    
        var tag = document.querySelector('downloads-manager').shadowRoot;
        var intag = tag.querySelector('downloads-item').shadowRoot;
        var file = intag.getElementById('file-link');
        
        return file.text;
        
        ''')
        # _browser.close()
        
        return progress
    def check_new_domain(self,_url,_await):
        d_new = True
        for domain  in self.blacklist:
            if domain in _url:
                return True
        if d_new:
            #VERIFICANDO ERRO DE INDISPONIBILIDADE PELO PORTAL CAPES
            try:
                warn = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#tr_1_basic1 > td:nth-child(2) > div > div > div.target > a')))
                if warn.text == 'O texto integral deste documento não está disponível via Portal .Periódicos.':
                    return True
            except Exception as e:
                with open('new-domains.txt','a+') as f:
                    f.write(_url+'\n')
                return False
    def expand_shadow_element(self,_element,_browser):
        shadow_root = _browser.execute_script('return arguments[0].shadowRoot', _element)
        return shadow_root
    def erro_log(self,_url):
        # REGISTRO DE DOMONIOS QUE POSSUEM UM LAYOUT DIFERENCIADO
        with open('log-erro.txt','a+') as f:
            f.write(_url+'\n')
    def _sciencedirect(self,_browser, _await):
        file_url =  _browser.current_url
        try:
            dl_button = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#mathjax-container > div.article-wrapper.u-padding-m-top.grid.row > article > div.PdfEmbed > div > a')))
            dl_button.click()
            _browser.switch_to.window(_browser.window_handles[-1])
            sleep(2)
            _browser.close()
        except Exception as e:
            #POPUP
            dl_button = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#pdfLink')))                
            try:
                dl_button.click()
                dl_button = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#popover-content-download-pdf-popover > div > div > a.link-button.u-margin-s-bottom.link-button-primary')))
                try:
                    dl_button.click()
                    _browser.switch_to.window(_browser.window_handles[-1])
                    sleep(2)
                    _browser.close()
                except Exception as e:
                    pass
            except Exception as e:
                pass
        return file_url
    def _projecteuclid(self,_browser, _await):
        file_url = None
        try:
            dl_button = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'body > div.main-content > div > div.thirteen.columns > div > section > div.download-buttons.box > div > a')))
            dl_button.click()
            sleep(2)
            file_url =  _browser.current_url
            _browser.close()
        except Exception as e:
            pass
        return file_url
    def _web_a_ebscohost(self,_browser, _await):
        #print('OLHAR AQUI!')
        input()
        file_url = None
        try:
            dl_button = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#ctl00_ctl00_Column1_Column1_formatButtonsTop_formatButtonRepeater_ctl02_linkButton')))
            dl_button.click()
            #selecionando o iframe
            try:
                iframe = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#pdfIframe')))
                file_url =  iframe.get_attribute('src')
                # _browser.switch_to_frame(iframe)
                _browser.close()   
            except Exception as e:
                pass
        except Exception as e:
            pass
        return file_url
    def _web_b_ebscohost(self,_browser, _await):
        #print('OLHAR AQUI2!!!')
        input()
        file_url = None
        try:
            dl_button = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#ctl00_ctl00_Column1_Column1_formatButtonsTop_formatButtonRepeater_ctl02_linkButton')))
            dl_button.click()
            #selecionando o iframe
            try:
                iframe = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#pdfIframe')))
                file_url =  iframe.get_attribute('src')
                # _browser.switch_to_frame(iframe)
                _browser.close()   
            except Exception as e:
                pass
        except Exception as e:
            pass
        return file_url
    def _link_springer_com(self,_browser, _await):
        try:
            dl_button = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#sidebar > aside > div:nth-child(1) > div > a')))
            dl_button.click()
            sleep(2)
        except Exception as e:
            try:
                dl_button = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#pdflink-container > div > a')))
                dl_button.click()
                sleep(2)
            except Exception as e:
                pass
    def _journals_sagepub_com(self,_browser, _await):    
        file_url = None
        try:
            dl_button = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#openAccessSideMenu > span:nth-child(2) > div > a')))
            dl_button.click()
            sleep(2)            
            file_url =  _browser.current_url
        except Exception as e:
            pass
        return file_url
    def _academic_oup_com(self,_browser, _await):
        file_url = None
        try:
            dl_button = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#Toolbar > li.toolbar-item.item-pdf > a')))
            file_url = dl_button.get_attribute('href')
            dl_button.click()
            sleep(2)
            
        except Exception as e:
            pass
        return file_url
    def _www_cambridge(self,_browser, _await):
        file_url = None
        try:
            dl_button = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#Top > div > div.overview.article-overview > div.abstract-text > div.article-actions > div > ul.file-actions > li:nth-child(2) > ul > li:nth-child(1) > a')))
            dl_button.click()
            sleep(2)
            _browser.switch_to.window(_browser.window_handles[2])
            file_url =  _browser.current_url
            _browser.close()
            _browser.switch_to.window(_browser.window_handles[1])
            _browser.close()
        except Exception as e:
            pass
        return file_url
    def _go_gale(self,_browser, _await):
        #TODO Resolver o problema de baixar automaticamente- gerenciar o download
        file_url = None
        try:
            dl_button = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#documentDisplay > section.document > div.document-tools.navigation.removeDrive > div.right > div > div.docTools-download.toolbar-button > button')))
            dl_button.click()        
            sleep(2)
            file_url = self.get_file_download_manager(_browser)
            
        
        except Exception as e:
            #print('Erro on Go GAle!')
            #print(e)
            #print('+++++++++++++++++++++++++++++')
            pass

        _browser.close()
        return file_url
    def _pubs_rsc_org(self,_browser, _await):
        file_url = None
        dl_button = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#DownloadOption > div > a.btn.btn--cta.btn--primary.btn--block.btn--stack.btn-icon.btn-icon--download')))
        dl_button.click()
        sleep(2)
        _browser.switch_to.window(_browser.window_handles[2])
        file_url =  _browser.current_url
        _browser.close()
        _browser.switch_to.window(_browser.window_handles[1])
        _browser.close()
        return file_url
    def _www_ncbi_nlm_nih_gov(self,_browser, _await):
        file_url = None
        try:
            dl_button = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#rightcolumn > div:nth-child(2) > div > ul > li:nth-child(4) > a')))
            file_url =  dl_button.get_attribute('href')
            _browser.close()
        except Exception as e:
            pass
        return file_url
    def _www_emerald(self,_browser, _await):
        # One click, new tab
        file_url = None
        try:
            dl_button = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#mainContent > div.bg-light.border-top.border-bottom.py-3.mb-3.content_block > div > div > div.col-12.col-md-8 > div > a.intent_pdf_link.text-uppercase.d-inline-block')))
            file_url = dl_button.get_attribute('href')
            _browser.get(file_url)
            sleep(2)
        except Exception as e:
            pass
        return file_url
    def _www_tandfonline(self,_browser, _await):
        # Link on button
        file_url = None
        try:
            dl_button = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#d29f04e9-776c-4996-a0d8-931023161e00 > div > div > div.publication-tabs.ja.publication-tabs-dropdown > div > ul > li.pdf-tab > a')))
            file_url =  dl_button.get_attribute('href')
            dl_button.click()
            sleep(2)
            _browser.close()
        except Exception as e:
            pass
        return file_url
    def _muse_jhu_edu(self,_browser,_await):
        # Link on button
        file_url = None
        try:
            dl_button = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#action_btns > li:nth-child(2) > a')))
            file_url =  dl_button.get_attribute('href')
            dl_button.click()
            sleep(2)
            _browser.close()
        except Exception as e:
            pass
        return file_url
    def _www_annualreviews_org(self,_browser, _await):
        # Link on button
        file_url = None
        try:
            dl_button = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#main-content > div > div > section.ar-content-left-col > article > div.article-info > div:nth-child(2) > div > a.btn.icon-pdf')))
            file_url =  dl_button.get_attribute('href')
            dl_button.click()
            sleep(2)
            _browser.close()
        except Exception as e:
            pass
        return file_url
    def _oecd_ilibrary_org(self,_browser, _await):
        # Link on button
        file_url = None
        try:
            dl_button = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#bellowheadercontainer > div > section.post-glimps.single-section.post-details-section.bgcolor-8 > div > div > div.col-xs-12.col-lg-9 > div > ul > li:nth-child(2) > a')))
            file_url =  dl_button.get_attribute('href')
            dl_button.click()
            sleep(2)
            _browser.close()
        except Exception as e:
            pass
        return file_url

    def _doaj(self,_browser, _await):
        # Link on another publisher
        file_url = None
        try:
            dl_button = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'div.col-md-10:nth-child(2) > div:nth-child(1) > p:nth-child(1) > strong:nth-child(1) > a:nth-child(1)')))            
            dl_button.click()
            current_url =  _browser.current_url
            for domain in self.model_law:
                if domain in current_url:
                    paper_link = self.model_law[domain](_browser,_await)
                    # #print(paper_link)
                    if paper_link:
                        file_url = paper_link
                    _browser.close()
                    break
        except Exception as e:
            pass
        return file_url
    def _openurl_ebscohost(self,_browser, _await):
        # One click, new tab
        file_url = None
        try:
            redirect_button = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#_ctl0_contentPh_ejsLink')))
            redirect_button.click()
            _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'body')))
            paper_url = _browser.current_url
            for domain in self.model_law:            
                if domain in paper_url:
                    # TODO: RESOLVER PROLEMA INTERMITENTE COM O ACESSO AOS PDFS
                    self.model_law[domain](_browser,_await)
                    break
                    
        except Exception as e:
            pass
        return paper_url
    def _onlinelibrary_wiley(self,_browser, _await):
        try:
            dl_button = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'div.cloned > a:nth-child(1)')))
            url = dl_button.get_attribute('href').replace('epdf','pdfdirect')
            _browser.get(url)
            sleep(5)            
            return dl_button.get_attribute('href')
        except Exception as e:
            pass
    def _scielo(self,_browser, _await):
        try:
            #First link
            dl_button = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'div.box:nth-child(5) > ul:nth-child(1) > li:nth-child(1)')))
            if 'pdf' in dl_button.text:
                dl_button.click()
            else:
                dl_button = _await.until(ec.visibility_of_element_located((By.CSS_SELECTOR,'div.box:nth-child(5) > ul:nth-child(1) > li:nth-child(2) > a:nth-child(1)')))
                dl_button.click()
            file_url = _browser.current_url()
            sleep(5)            
            return file_url
        except Exception as e:
            pass

