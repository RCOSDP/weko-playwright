from tkinter import ON
import pytest
import configparser
from playwright.sync_api import sync_playwright

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

    # Click input[name="pubdate"]
    page.click("input[name=\"pubdate\"]")

    # Click text="02"
    page.click("text=\"02\"")

    page.screenshot(path=f'{"Autotest03_043_1"}_capture.png')

    # Fill input[name="item_1617186331708.0.subitem_1551255647225"]
    page.fill("input[name=\"item_1617186331708.0.subitem_1551255647225\"]", "登録テストアイテム1")

    # Click input[name="item_1617186331708.0.subitem_1551255647225"]
    page.click("input[name=\"item_1617186331708.0.subitem_1551255647225\"]")

    page.screenshot(path=f'{"Autotest03_044_1"}_capture.png')

    # Select string:ja
    page.select_option("//div[normalize-space(.)='jaja-Kanaenfritdeeszh-cnzh-twrulamseoarelko']/select", "string:ja")

    page.screenshot(path=f'{"Autotest03_045_1"}_capture.png')

    # Select string:conference paper
    page.select_option("//div[starts-with(normalize-space(.), 'conference paperdata paperdepartmental bulletin papereditorialjournal articlenew')]/select", "string:conference paper")
    page.wait_for_timeout(int(SET_WAIT))
    page.screenshot(path=f'{"Autotest03_046_1"}_capture.png')

    # Click text=/.*Save.*/
    page.click("text=/.*Save.*/")
    # assert page.url == "https://localhost/workflow/activity/detail/A-20220203-00001?status="

    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)