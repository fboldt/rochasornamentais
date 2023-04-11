import sys
import os
import json
from time import sleep
from datetime import datetime
# from pprint import pprint

import pandas as pd
import numpy as np
import bibtexparser

import selenium
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from decouple import config


if not os.path.exists('download'):
    os.makedirs('download')
if not os.path.exists('data'):
    os.makedirs('data')
if not os.path.exists('plot'):
    os.makedirs('plot')


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
        executable_path=r'./chromedriver.exe' if os.name == 'nt' else r'./chromedriver', options=options)

    _await = WebDriverWait(browser, 30)
    browser.get(url)

    return browser, _await


def _get_credentials():
    return {'login': config('LOGIN'), 'password': config('PASSWORD')}


def _login_CAFe(_await, browser):
    credentials = _get_credentials()
    login = credentials['login']
    password = credentials['password']

    try:
        browser.find_element_by_css_selector(
            '#username').send_keys(login)
        browser.find_element_by_css_selector(
            '#password').send_keys(password)

        browser.find_element_by_css_selector(
            '#login-main-content > div.loginMainContentLoginBox.clearfix > form > button').click()

        _await.until(ec.visibility_of_element_located(
            (By.CSS_SELECTOR, '#attribute-release-main-content > div.attributeReleaseMainContent.clearfix > div:nth-child(2) > div.button > ul > li:nth-child(2) > button'))).click()
    except Exception as err:
        print(err)


def _get_url_login(browser, _await):
    institute = 'IFES - INSTITUTO FEDERAL DO ESPÍRITO SANTO'

    try:
        _await.until(ec.visibility_of_element_located(
            (By.CSS_SELECTOR, 'body > footer > div.container.container-menus > div.row-fluid > div > div > div.modal-footer > button'))).click()
    except:
        pass

    select = browser.find_element_by_css_selector('#listaInstituicoesCafe')
    for option in select.find_elements_by_tag_name('option'):
        if option.get_attribute('text') == institute:
            return option.get_attribute('value').replace('#', '.')

    return 404


def login(browser, _await):
    url_login = _get_url_login(browser, _await)
    if url_login == 404:
        print('page not found')
        return 0
    browser.get(url_login)
    sleep(5)
    _login_CAFe(_await, browser)


def _search_scopus(browser, _await, query, first_iterable):
    url = 'https://buscador-periodicos-capes-gov-br.ez120.periodicos.capes.gov.br/V/VIPQP1VHE7UHNHD6KPDEHT64J7BLXH69KC7435AMIXMGRK83YF-14911?func=native-link&resource=CAP04092'
    browser.get(url)

    try:
        _await.until(ec.visibility_of_element_located(
            (By.ID, '_pendo-close-guide_'))).click()
    except TimeoutException:
        try:
            _await.until(ec.visibility_of_element_located(
                (By.CLASS_NAME, '_pendo-close-guide'))).click()
        except TimeoutException:
            pass
    except:
        pass

    if not first_iterable:
        browser.find_element_by_css_selector(
            '#documents-tab-panel > div > micro-ui > scopus-document-search-form > form > div:nth-child(3) > div > div.keyword-wrapper.DocumentSearchForm__flexAuto___301CQ.DocumentSearchForm__width60___2C1nw > els-input > div > label > input').clear()

    browser.find_element_by_css_selector(
        '#documents-tab-panel > div > micro-ui > scopus-document-search-form > form > div:nth-child(3) > div > div.keyword-wrapper.DocumentSearchForm__flexAuto___301CQ.DocumentSearchForm__width60___2C1nw > els-input > div > label > input').send_keys(query)

    browser.find_element_by_css_selector(
        '#DocumentSearchForm__submitButton___16LlX').click()

    try:
        _await.until(ec.visibility_of_element_located(
            (By.ID, '_pendo-close-guide_'))).click()
    except TimeoutException:
        try:
            _await.until(ec.visibility_of_element_located(
                (By.CLASS_NAME, '_pendo-close-guide'))).click()
        except TimeoutException:
            pass
    except:
        pass

    try:
        error = _await.until(ec.visibility_of_element_located(
            (By.CSS_SELECTOR, '#main-content > div.alert.alert-danger > div > div > h4'))).text
        if error:
            print(query, error, 'Scopus')
            return 0
    except:
        pass

    browser.find_element_by_css_selector('#selectAllCheck').click()
    browser.find_element_by_css_selector('#export_results').click()
    sleep(5)

    if first_iterable:
        browser.find_element_by_css_selector(
            '#bibliographicalInformationCheckboxes').click()
        browser.find_element_by_css_selector(
            '#abstractInformationCheckboxes').click()
        browser.find_element_by_css_selector(
            '#fundInformationCheckboxes').click()
        browser.find_element_by_css_selector(
            '#otherInformationCheckboxes > span > label').click()
        browser.find_element_by_css_selector(
            '#exportList > li:nth-child(5)').click()

    browser.find_element_by_css_selector('#exportTrigger').click()
    sleep(10)


def search(browser, _await, queries):
    first_iterable = True

    for query in queries:
        print('\nSearch: {}'.format(query))
        _search_scopus(browser, _await, query, first_iterable)

        if first_iterable:
            first_iterable = False


def _move_files():
    CURRENT_USER = os.path.expanduser('~')
    DOWNLOAD_PATH = os.listdir(CURRENT_USER + '/Downloads')

    for file_name in DOWNLOAD_PATH:
        _file = file_name.split('.')
        if 'bib' == _file[len(_file) - 1] and _file[0].startswith('scopus'):
            src = CURRENT_USER + '/Downloads/' + file_name
            dst = r'./download/' + file_name

            print('\nMoving', src, dst)
            os.rename(src, dst)
        else:
            continue


def _write_data(file_name, values):
    try:
        os.remove('./data/'+file_name+'.json')
    except:
        pass
    with open('./data/'+file_name+'.json', 'w', encoding='utf8') as f:
        json.dump(values, f, ensure_ascii=False, indent=2)


def merge_and_drop_duplicates():
    dataframes = []
    files = os.listdir('./download')
    for f in files:
        _file = r'./download/' + f
        with open(_file, encoding='utf8') as output:
            bib_data = bibtexparser.load(output)
        df = pd.DataFrame(bib_data.entries)
        dataframes.append(df)

    # Unir e retirar duplicatas
    df_merge = pd.concat(dataframes)
    df_merge = df_merge.drop_duplicates(subset='ID', keep="first")

    print('Generate raw data JSON')
    result = df_merge.to_json(orient='records')
    parsed = json.loads(result)

    _write_data('rawdata', parsed)


def pre_process():
    processed = []
    f = open('./data/rawdata.json', encoding='utf8')
    rawdata = json.load(f)
    for value in rawdata:
        # get articles
        if value['document_type'].lower() == 'article':
            if value['language'] != None and (value['language'].lower() != 'portuguese' and value['language'].lower() != 'english' and value['language'].lower() != 'english; portuguese'):
                continue

            if int(value['year']) < 2003 or int(value['year']) >= 2020:
                continue

            references_count = 0
            if value['references'] != None:
                references_count = len(value['references'].split(';'))

            if value['author_keywords'] != None:
                keyword_count = len(value['author_keywords'].split(';'))
                value['keywords'] = value['author_keywords']
            elif value['keywords'] != None:
                keyword_count = len(value['keywords'].split(';'))
            else:
                keyword_count = 0

            value['references_count'] = references_count
            value['keyword_count'] = keyword_count
            processed.append(value)

    _write_data('processeddata', processed)


def main(args):
    START = datetime.now()
    print('\nStart: {}\n'.format(START))

    # inicia busca
    queries = ["ornamental stone OR ornamental rock OR rocha ornamental OR marble OR mármore OR granite OR granito",
               "waste OR residue OR sludge OR powder OR dust OR slurry OR tailing AND rejeito OR resíduo OR lama OR lodo",
               "civil construction OR construção civil OR civil engineering OR engenharia civil OR construction material OR material de construção"]

    print('Init browser\n')
    browser, _await = initialize_browser()

    print('\nLogin CAFe\n')
    login(browser, _await)

    print('Init Search')
    search(browser, _await, queries)

    sleep(30)
    print('\nExit Scrapper')
    browser.quit()

    print('\nMoving downloaded files')
    _move_files()

    print('\nMerge raw data and remove duplicates')
    merge_and_drop_duplicates()

    # pre processando
    print('Pre process data')
    pre_process()
    print('Pre process data created in data/')

    # print('Ploting')
    # import coocurance
    # import freq_year

    print('\nDuration: {}'.format(datetime.now() - START))

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
