from loginCAFe import login
from database import Connection
from initBrowser import initialize_browser
import selenium
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from time import sleep
from decouple import config


def _search_wos(_await, browser, query, first_iterable):
    url = 'https://buscador-periodicos-capes-gov-br.ez120.periodicos.capes.gov.br/V/FLN2ME3QNMTNN6FJXFKGM6RE79Q99IFL4P3TX5RKJRLCUPVF63-04064?func=native-link&resource=CAP00731'

    browser.get(url)
    sleep(10)

    if (not first_iterable):
        _await.until(ec.visibility_of_element_located((
            By.CSS_SELECTOR,
            'input.focusinput.search-criteria-input'))).clear()

    _await.until(ec.visibility_of_element_located(
        (By.CSS_SELECTOR, 'input.focusinput.search-criteria-input'))).send_keys(query)

    if first_iterable:
        browser.find_element(
            By.CSS_SELECTOR, '#select2-select1-container').click()
        browser.find_element(
            By.CSS_SELECTOR, '#select2-select1-results > li:nth-child(8)').click()
        browser.find_element(
            By.CSS_SELECTOR, '#addSearchRow1 > a:nth-child(1)').click()
        browser.find_element(
            By.CSS_SELECTOR, '#select2-select2-container').click()
        browser.find_element(
            By.CSS_SELECTOR, '#select2-select2-results > li:nth-child(14)').click()
        browser.find_element(
            By.CSS_SELECTOR, '.select2-selection__choice__remove').click()
        browser.find_element(
            By.CSS_SELECTOR, '#select2-value\(input2\)-results > li:nth-child(2)').click()

    sleep(5)
    _await.until(ec.visibility_of_element_located((
        By.CSS_SELECTOR, '#searchCell2 > span.searchButton > button'))).click()

    try:
        error = _await.until(ec.visibility_of_element_located((
            By.CSS_SELECTOR,
            '#noRecordsDiv > div.newErrorHead'))).text
        if error:
            print(query, error, 'WOS')
            return 0
    except:
        pass
    sleep(15)

    count = _await.until(ec.visibility_of_element_located(
        (By.CSS_SELECTOR, '#hitCount\.top'))).text

    _await.until(ec.visibility_of_element_located((
        By.CSS_SELECTOR, '#exportTypeName'))).click()

    if first_iterable:
        browser.find_element(
            By.CSS_SELECTOR, '#saveToMenu > li:nth-child(4) > a').click()

    browser.find_element(
        By.CSS_SELECTOR, '#select2-bib_fields-container').click()
    browser.find_element(
        By.CSS_SELECTOR, '#select2-bib_fields-results > li:nth-child(4)').click()
    browser.find_element(
        By.CSS_SELECTOR, '#select2-saveOptions-container').click()
    browser.find_element(
        By.CSS_SELECTOR, '#select2-saveOptions-results > li:nth-child(2)').click()

    try:
        browser.find_element(
            By.CSS_SELECTOR, '#numberOfRecordsRange').click()
    except:
        pass

    browser.find_element(By.CSS_SELECTOR, '#exportButton').click()
    sleep(10)

    return count


def _search_scopus(_await, browser, query, first_iterable):
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
        browser.find_element_by_css_selector('#searchterm1').clear()

    browser.find_element_by_css_selector('#searchterm1').send_keys(query)

    if first_iterable:
        browser.find_element_by_css_selector('#field1-button').click()
        browser.find_element_by_css_selector(
            '#field1-menu > li:nth-child(1)').click()
        sleep(5)
    browser.find_element_by_css_selector('#searchBtnRow > button').click()

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

    try:
        count = browser.find_element(
            By.CSS_SELECTOR, '#searchResFormId > div:nth-child(2) > div > header > h1 > span.resultsCount').text
    except:
        count = 0

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
            '#otherInformationCheckboxes').click()
        browser.find_element_by_css_selector(
            '#exportList > li:nth-child(5)').click()

    browser.find_element_by_css_selector('#exportTrigger').click()
    sleep(5)

    return count


def _get_querys(conn):
    if config('PYTHON_ENV') == 'production':
        return conn.get_all('query')
    queries = []
    f = open('./query.txt', encoding='utf8')
    for line in f:
        queries.append(line.rstrip('\n'))
    return queries


def _save_query_count(query, wos, scopus):
    try:
        conn = Connection()
        conn.insert('query_count', {'query': query,
                                    'wos': wos, 'scopus': scopus})
        conn.close()
    except Exception as e:
        print(e)
        return False


def _search(browser, _await, query, first_iterable):
    wos = _search_wos(_await, browser, query, first_iterable)
    scopus = _search_scopus(_await, browser, query, first_iterable)

    _save_query_count(query, wos, scopus)


def _init_search(browser, _await, queries):
    first_iterable = True

    if config('PYTHON_ENV') == 'production':
        for query in queries:
            if not query['used']:
                print('\nSearch {}'.format(query['query']))
                _search(browser, _await, query['query'], first_iterable)
                conn = Connection()
                conn.update_one('query', {'id': query['_id']}, {'used': True})
                conn.close()

                if first_iterable:
                    first_iterable = False
        return

    for query in queries:
        print('\nSearch {}'.format(query))
        _search(browser, _await, query, first_iterable)
        conn = Connection()
        conn.insert('query', {'query': query, 'used': True})
        conn.close()

        if first_iterable:
            first_iterable = False


def init():
    conn = Connection()
    queries = _get_querys(conn)

    print('Init browser\n')
    browser, _await = initialize_browser()

    print('\nLogin CAFe\n')
    login(browser, _await)

    print('Init Search\n')
    _init_search(browser, _await, queries)

    sleep(30)
    print('Exit Scrapper\n')
    browser.quit()
