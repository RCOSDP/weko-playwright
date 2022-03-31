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

    # Click text=/.*Log in.*/
    page.click("text=/.*Log in.*/")
    # assert page.url == "https://localhost/login/?next=%2F"

    # Fill input[name="email"]
    page.fill("input[name=\"email\"]", "comadmin@example.org")

    # Fill input[name="password"]
    page.fill("input[name=\"password\"]", "uspass123")

    # Click text=/.*Log In.*/
    page.click("text=/.*Log In.*/")
    # assert page.url == "https://localhost/"

    # Click //div[normalize-space(.)='Index A']/div[1]
    page.click("//*[@id='index-background']/app-tree-items/app-tree-list2/div/div/div/tree/tree-internal/ul/li/tree-internal[1]/ul/li/div/div[2]/span")

    # Click text="title"        
    #　一度編集すると、同じアイテムは編集できなくなるので「div[11]/div[1]/div/a"」のdiv[11]の値を変更すること
    page.click("//*[@id='index_item_list']/div[2]/div/div/invenio-search-results/div[11]/div[1]/div/a")

    page.wait_for_timeout(int(SET_WAIT)*2)

    page.screenshot(path=f'{path.splitext(path.basename(__file__))[0]+"_1"}_capture.png')

    page.wait_for_timeout(int(SET_WAIT))

    # Click text=/.*Edit.*/
    page.click("//*[@id='btn_edit']")
    # assert page.url == "https://localhost/records/301#/!"
    page.screenshot(path=f'{path.splitext(path.basename(__file__))[0]+"_2"}_capture.png')

    # Press ArrowDown
    # page.press("//div[normalize-space(.)='jaja-Kanaenfritdeeszh-cnzh-twrulamseoarelko']/select", "ArrowDown")
    page.press("//*[@id='weko-records']/invenio-files-uploader/invenio-records/div[2]/div[8]/invenio-records-form/div/div/form/bootstrap-decorator[2]/fieldset/div/div[2]/div/div[1]/ol/li[1]/sf-decorator/div/sf-decorator[2]/div/div/select", "ArrowDown")

    # Fill input[name="radioVersionSelect"]
    # page.fill("input[name=\"radioVersionSelect\"]", "update")
    page.click("//*[@id='react-component-version']/div/div/div/div[1]/input")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{path.splitext(path.basename(__file__))[0]+"_3"}_capture.png')

    page.click("//*[@id='react-component-version']/div/div/div/div[2]/input")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{path.splitext(path.basename(__file__))[0]+"_4"}_capture.png')

    # Click text=/.*Next.*/
    page.click("text=/.*Next.*/")
    # assert page.url == "https://localhost/workflow/activity/detail/A-20220225-00008"

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