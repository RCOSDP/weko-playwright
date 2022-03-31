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
 
    # Click //a[normalize-space(.)='Index Tree']
    page.click("//a[normalize-space(.)='Index Tree']")

    # Click text="Edit Tree"
    page.click("text=\"Edit Tree\"")
    # assert page.url == "https://localhost/admin/indexedit/"

    # Click //tree-internal[83]/ul/li/div/div[2]/span[normalize-space(.)='New Index']
    page.click("text=/.*New Index.*/")

    page.wait_for_timeout(int(SET_WAIT))

    # Fill input[type="text"]
    page.fill("input[type=\"text\"]", "Nini")

    # Fill //div[normalize-space(.)='English＊']/input[normalize-space(@type)='text']
    page.fill("//div[normalize-space(.)='English＊']/input[normalize-space(@type)='text']", "")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{path.splitext(path.basename(__file__))[0]+"_2"}_capture.png')

    # Click text=/.*Click to select.*/
    with page.expect_file_chooser() as fc_info:
        page.click("text=/.*Choose File.*/")
    file_chooser = fc_info.value
    file_chooser.set_files("sample.bmp")

    page.wait_for_timeout(int(SET_WAIT))

    # Click text=/.*Send.*/
    page.click("text=/.*Send.*/")

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