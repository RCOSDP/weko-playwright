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

    page.screenshot(path=f'{path.splitext(path.basename(__file__))[0]+"_1"}_capture.png')

    # Press ArrowUp
    page.press("select[id=\"selectedDisplay\"]", "ArrowUp")
    page.press("select[id=\"selectedDisplay\"]", "ArrowUp")
    page.press("select[id=\"selectedDisplay\"]", "ArrowUp")
    page.press("select[id=\"selectedDisplay\"]", "ArrowUp")
    # assert page.url == "https://localhost/search?page=1&size=20&sort=upd&timestamp=1647231059.38236&search_type=0&q="

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{path.splitext(path.basename(__file__))[0]+"_2"}_capture.png')

    # Press ArrowDown
    page.press("select[id=\"pagesize\"]", "ArrowDown")
    # assert page.url == "https://localhost/search?page=1&size=50&sort=-createdate&timestamp=1647231377.5822868&search_type=0&q="

    # Click input[name="search_type"]
    page.click("input[name=\"search_type\"]")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{"Autotest05_040_1"}_capture.png')

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