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
    page.fill("input[name=\"email\"]", "wekosoftware@nii.ac.jp")

    # Fill input[name="password"]
    page.fill("input[name=\"password\"]", "uspass123")

    # Click text=/.*Log In.*/
    page.click("text=/.*Log In.*/")
    # assert page.url == "https://localhost/"

    page.click("text=\"Top\"")

    # Click //button
    page.click("//button")

    # Click text=/.*Administration.*/
    page.click("text=/.*Administration.*/")
    # assert page.url == "https://localhost/admin/"

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{path.splitext(path.basename(__file__))[0]+"_1"}_capture.png')

    # Click //a[normalize-space(.)='WorkFlow']
    page.click("//a[normalize-space(.)='WorkFlow']")

    # Click //a[normalize-space(.)='Web Design']/i
    page.click("//a[normalize-space(.)='Web Design']/i")

    # Click text="Widget"
    page.click("text=\"Widget\"")
    # assert page.url == "https://localhost/admin/widgetitem/"

    # Click text="List"
    # page.click("text=\"List\"")
    page.click("//html/body/div[1]/div/section[2]/ul/li[1]/a")
    # assert page.url == "https://localhost/admin/widgetitem/"

    # Click //a[normalize-space(@title)='View Record']/span
    page.click("//a[normalize-space(@title)='View Record']/span")
    # assert page.url == "https://localhost/admin/widgetitem/details/?id=1&url=/admin/widgetitem/"

    page.wait_for_timeout(int(SET_WAIT))
    
    page.screenshot(path=f'{"Autotest05_438_1"}_capture.png')

    # Click text="List"
    # page.click("text=\"List\"")
    page.click("//html/body/div[1]/div/section[2]/ul/li[1]/a")
    # assert page.url == "https://localhost/admin/widgetitem/"

    page.wait_for_timeout(int(SET_WAIT))
    
    page.screenshot(path=f'{"Autotest05_439_1"}_capture.png')

    # Click text="ID"
    page.click("text=\"ID\"")
    # assert page.url == "https://localhost/admin/widgetitem/?sort=0"

    page.wait_for_timeout(int(SET_WAIT))
    
    page.screenshot(path=f'{"Autotest05_439_2"}_capture.png')

    # Click //a[normalize-space(.)='Widget Type' and normalize-space(@title)='Sort by Widget Type']
    page.click("//a[normalize-space(.)='Widget Type' and normalize-space(@title)='Sort by Widget Type']")
    # assert page.url == "https://localhost/admin/widgetitem/?sort=2"

    page.wait_for_timeout(int(SET_WAIT))
    
    page.screenshot(path=f'{"Autotest05_439_3"}_capture.png')

    # Click //a[normalize-space(.)='Enable' and normalize-space(@title)='Sort by Enable']
    page.click("//a[normalize-space(.)='Enable' and normalize-space(@title)='Sort by Enable']")
    # assert page.url == "https://localhost/admin/widgetitem/?sort=4"

    page.wait_for_timeout(int(SET_WAIT))
    
    page.screenshot(path=f'{"Autotest05_439_4"}_capture.png')

        # Click text=/.*Add Filter.*/
    page.click("text=/.*Add Filter.*/")

    # Click text="Repository"
    page.click("text=\"Repository\"")

    # Click //a[normalize-space(.)='Add Filter']/b
    page.click("//a[normalize-space(.)='Add Filter']/b")

    # Click text="Widget Type"
    page.click("text=\"Widget Type\"")

    # Click //a[normalize-space(.)='Add Filter']/b
    page.click("//a[normalize-space(.)='Add Filter']/b")

    # Click text="Enable"
    page.click("text=\"Enable\"")

    page.wait_for_timeout(int(SET_WAIT))
    
    page.screenshot(path=f'{"Autotest05_440_1"}_capture.png')

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