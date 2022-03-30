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

    # Click text="Workflow"
    page.click("text=\"Workflow\"")
    # assert page.url == "https://localhost/workflow/"

    if SET_WFDAY == "NEW":
        # Click text=/.*New Activity.*/
        page.click("text=/.*New Activity.*/")

        with page.expect_navigation():
            page.click("//tr[3]/td[4]/button[normalize-space(.)='  New']")
    else:
        # Go to https://localhost/workflow/activity/detail/A-20220203-00001
        page.goto("https://localhost/workflow/activity/detail/A-" + SET_WFDAY,timeout=int(SET_TIMEOUT))

    # Click div[id="activity_locked"] >> text="OK"
    if ACTIVE_LOCK == "ON":
        page.click("div[id=\"activity_locked\"] >> text=\"OK\"")
    # assert page.url == "https://localhost/workflow/activity/detail/A-20220203-00001?status="

    # Click text=/.*Creator.*/
    page.click("text=/.*Creator.*/")

    # Click text=/.*著者DBから入力.*/
    page.click("text=/.*著者DBから入力.*/")

    page.wait_for_timeout(int(SET_WAIT))

    page.click("text=\"Add Author\"")

    # Fill input[placeholder="セイ"]
    page.fill("input[placeholder=\"セイ\"]", "情報")

    # Fill input[placeholder="メイ"]
    page.fill("input[placeholder=\"メイ\"]", "太郎")

    page.press('//*[@id="authorIdOption"]', "ArrowDown")
   
    # Fill //div[normalize-space(.)='+  Add E-mail']/div[1]/div/div[1]/input[normalize-space(@type)='text']
    # page.fill("//div[normalize-space(.)='+  Add E-mail']/div[1]/div/div[1]/input[normalize-space(@type)='text']", "wekosoftware@nii.ac.jp")
    page.fill('//*[@id="app-author-search"]/div/div/div[1]/app-author-search/div/div/app-add-author/div[2]/div/div/div/div[3]/div/div[2]/div[1]/div/div[1]/input', "wekosoftware@nii.ac.jp")
                
    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{path.splitext(path.basename(__file__))[0]+"_1"}_capture.png')

    page.click('//*[@id="app-author-search"]/div/div/div[1]/app-author-search/div/div/app-add-author/div[2]/div/div/div/div[4]/div[2]/button[2]')
   
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