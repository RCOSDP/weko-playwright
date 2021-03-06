__file__
import pytest
import configparser
from playwright.sync_api import sync_playwright
from os import path

config_ini = configparser.ConfigParser()
config_ini.read( "conf.ini", encoding = "utf-8" )
print("SET_TIMEOUT = " + config_ini['DEFAULT']['SETTIMEOUT'])
print("SET_WAIT = " + config_ini['DEFAULT']['SETWAIT'])
print("SET_WAIT = " + config_ini['DEFAULT']['SETWFDAY'])
print("ACTIVE_LOCK = " + config_ini['DEFAULT']['ACTIVELOCK'])
print("WEKO_URL = " + config_ini['DEFAULT']['WEKOURL'])
SET_TIMEOUT = config_ini['DEFAULT']['SETTIMEOUT']
SET_WAIT = config_ini['DEFAULT']['SETWAIT']
SET_WFDAY = config_ini['DEFAULT']['SETWFDAY']
ACTIVE_LOCK = config_ini['DEFAULT']['ACTIVELOCK']
WEKO_URL = config_ini['DEFAULT']['WEKOURL']

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(ignore_https_errors=True)

    # Open new page
    page = context.new_page()

    # Go to https://localhost/
    page.goto(WEKO_URL,timeout=int(SET_TIMEOUT))

    page.click("text=\"Top\"")
   
    # Click text=/.*Full text.*/
    page.click("text=/.*Full text.*/")

    # Click text="Search"
    # with page.expect_navigation(url="https://localhost/search?page=1&size=20&sort=-createdate&timestamp=1647225954.063391&search_type=0&q=登録テスト"):
    with page.expect_navigation():
        page.click("text=\"Search\"")

    page.wait_for_timeout(int(SET_WAIT))

    page.click('//*[@id="index_item_list"]/div[2]/div/div/invenio-search-results/div[2]/div[1]/div/a')

    page.wait_for_timeout(int(SET_WAIT))
    
    # Click text=/.*Full text.*/
    page.click("text=/.*Full text.*/")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{path.splitext(path.basename(__file__))[0]+"_1"}_capture.png')

    # page.click('//*[@id="invenio-csl"]/div[3]/div[2]/invenio-csl/invenio-csl-typeahead/span/input[2]')
    page.click("text=/.*Share.*/")

    page.wait_for_timeout(int(SET_WAIT))
    
    page.screenshot(path=f'{"Autotest05_055_1"}_capture.png')

    # with page.expect_navigation():
    with page.expect_popup() as popup_info:
        page.click("svg[role=\"img\"]")
    page1 = popup_info.value
    
    page1.click('//*[@id="bdd-email"]')

    page1.wait_for_timeout(int(SET_WAIT))
    
    page1.screenshot(path=f'{path.splitext(path.basename(__file__))[0]+"_2"}_capture.png')

    # Close page
    page1.close()

    with page.expect_popup() as popup_info:
        page.click(".at-icon.at-icon-twitter g path")
    page2 = popup_info.value

    # Click input[name="session[username_or_email]"]
    page2.click("input[name=\"session[username_or_email]\"]")

    page2.wait_for_timeout(int(SET_WAIT))

    page2.screenshot(path=f'{"Autotest05_056_1"}_capture.png')

    # Close page
    page2.close()

    with page.expect_popup() as popup_info:
        page.click(".at-icon.at-icon-facebook g path")
    page3 = popup_info.value

    # Click input[name="email"]
    page3.click("input[name=\"email\"]")

    page3.wait_for_timeout(int(SET_WAIT))

    page3.screenshot(path=f'{"Autotest05_057_1"}_capture.png')

    # Close page
    page3.close()

    page.click(".at-icon.at-icon-print g path")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{"Autotest05_058_1"}_capture.png')

    page.wait_for_timeout(int(SET_WAIT))

    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()

    return 0

def test_OK():
    assert a == 0

with sync_playwright() as playwright:
    a = run(playwright)
    test_OK()