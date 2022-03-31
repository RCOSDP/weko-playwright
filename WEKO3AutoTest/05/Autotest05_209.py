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

    page.wait_for_timeout(int(SET_WAIT))

    # Click text=/.*Click to select.*/
    with page.expect_file_chooser() as fc_info:
        page.click("text=/.*Click to select.*/")
    file_chooser = fc_info.value
    file_chooser.set_files("sample.pdf")

    # Click text="Start upload"
    page.click("text=\"Start upload\"")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{path.splitext(path.basename(__file__))[0]+"_1"}_capture.png')

    # Click //a[normalize-space(.)='File']/span[1]/i
    page.click('//*[@id="weko-records"]/invenio-files-uploader/invenio-records/div[2]/div[8]/invenio-records-form/div/div/form/bootstrap-decorator[1]/fieldset/div/div[1]/a')

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{path.splitext(path.basename(__file__))[0]+"_2"}_capture.png')

    #page.select_option("//div[normalize-space(.)='DetailSimplePreview']/select", "string:Detail")
    page.press("//div[normalize-space(.)='DetailSimplePreview']/select", "ArrowDown")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{path.splitext(path.basename(__file__))[0]+"_3"}_capture.png')

    #page.select_option("//div[starts-with(normalize-space(.), 'write your own licenseCreative Commons CC0 1.0 Universal Public Domain Designati')]/select", "string:Creative Commons CC0 1.0")
    page.press("//div[starts-with(normalize-space(.), 'write your own licenseCreative Commons CC0 1.0 Universal Public Domain Designati')]/select", "ArrowDown")
    page.press("//div[starts-with(normalize-space(.), 'write your own licenseCreative Commons CC0 1.0 Universal Public Domain Designati')]/select", "ArrowDown")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{"Autotest05_241_1"}_capture.png')

    # Click //label[normalize-space(.)='Input Open Access Date']/input[normalize-space(@type)='radio' and normalize-space(@name)='item_1617605131499.0.accessrole']
    page.click("//label[normalize-space(.)='Input Open Access Date']/input[normalize-space(@type)='radio' and normalize-space(@name)='item_1617605131499.0.accessrole']")

    # Click input[name="dateValue"]
    page.click("input[name=\"dateValue\"]")

    # Click text="01"
    page.click("text=\"01\"")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{"Autotest05_255_1"}_capture.png')

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