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

    # Click //a[normalize-space(.)='Item Types']
    page.click("//a[normalize-space(.)='Item Types']")

    # Click text="Metadata"
    page.click("text=\"Metadata\"")
    # assert page.url == "https://localhost/admin/itemtypes/"

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{path.splitext(path.basename(__file__))[0]+"_1"}_capture.png')
 
    # Click text=/.*New Registration.*/ >> input[name="radio_versionup"]
    page.click("text=/.*New Registration.*/ >> input[name=\"radio_versionup\"]")

    # Click text=/.*Add Metadata.*/
    page.click("text=/.*Add Metadata.*/")

    # Click input[placeholder="Input Type Name"]
    page.click("input[placeholder=\"Input Type Name\"]")

    # Fill input[placeholder="Input Type Name"]
    page.fill("input[placeholder=\"Input Type Name\"]", "テストアイテムタイプ10")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{path.splitext(path.basename(__file__))[0]+"_2"}_capture.png')

    # Click text=/.*Save.*/
    # with page.expect_navigation(url="https://localhost/admin/itemtypes/19"):
    with page.expect_navigation():
        page.click("text=/.*Save.*/")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{path.splitext(path.basename(__file__))[0]+"_3"}_capture.png')

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