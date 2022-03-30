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
SET_TIMEOUT = config_ini['DEFAULT']['SETTIMEOUT']
SET_WAIT = config_ini['DEFAULT']['SETWAIT']
SET_WFDAY = config_ini['DEFAULT']['SETWFDAY']
ACTIVE_LOCK = config_ini['DEFAULT']['ACTIVELOCK']

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(ignore_https_errors=True)

    # Open new page
    page = context.new_page()

    # Go to https://localhost/
    page.goto("https://localhost/",timeout=int(SET_TIMEOUT))

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
 
    # Click //a[normalize-space(.)='Item Types']
    page.click("//a[normalize-space(.)='Item Types']")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{path.splitext(path.basename(__file__))[0]+"_1"}_capture.png')

    # Click text="Metadata"
    page.click("text=\"Metadata\"")
    # assert page.url == "https://localhost/admin/itemtypes/"

    # Standard Item Type 
    page.click("//html/body/div/div/section[2]/div[1]/div/div/div/div[1]/label[1]/input")

    # Press ArrowDown
    page.press("select[id=\"item-type-lists\"]", "ArrowDown")
    page.press("select[id=\"item-type-lists\"]", "ArrowDown")
    page.press("select[id=\"item-type-lists\"]", "ArrowDown")
    # assert page.url == "https://localhost/admin/itemtypes/15"

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{path.splitext(path.basename(__file__))[0]+"_2"}_capture.png')

    page.wait_for_timeout(int(SET_WAIT))

    # Press ArrowUp
    page.press("select[id=\"item-type-lists\"]", "ArrowUp")
    # assert page.url == "https://localhost/admin/itemtypes/15" 

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{"Autotest05_143_1"}_capture.png')


    # Fill text="Item Type for Harvesting" >> input[name="item_type"] 
    page.click("//html/body/div/div/section[2]/div[1]/div/div/div/div[1]/label[2]/input")

    # Press ArrowUp
    page.press("select[id=\"item-type-lists\"]", "ArrowUp")
    # assert page.url == "https://localhost/admin/itemtypes/15"

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{"Autotest05_146_1"}_capture.png')

    # Fill text="Deleted Item Type" >> input[name="item_type"]
    page.click("//html/body/div/div/section[2]/div[1]/div/div/div/div[1]/label[3]/input")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{"Autotest05_147_1"}_capture.png')

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