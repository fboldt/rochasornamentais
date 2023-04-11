import selenium
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from time import sleep
from decouple import config


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
    sleep(10)
    _login_CAFe(_await, browser)
