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


    # Click text=/.*Bibliographic Information.*/
    page.click("text=/.*Bibliographic Information.*/")

    # Fill input[name="item_1617187056579.bibliographicVolumeNumber"]
    page.fill("input[name=\"item_1617187056579.bibliographicVolumeNumber\"]", "100")

    # Fill input[name="item_1617187056579.bibliographicIssueNumber"]
    page.fill("input[name=\"item_1617187056579.bibliographicIssueNumber\"]", "100")

    # Fill input[name="item_1617187056579.bibliographicPageStart"]
    page.fill("input[name=\"item_1617187056579.bibliographicPageStart\"]", "1")

    # Fill input[name="item_1617187056579.bibliographicPageEnd"]
    page.fill("input[name=\"item_1617187056579.bibliographicPageEnd\"]", "100")

    # Fill input[name="item_1617187056579.bibliographicNumberOfPages"]
    page.fill("input[name=\"item_1617187056579.bibliographicNumberOfPages\"]", "100")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{path.splitext(path.basename(__file__))[0]+"_1"}_capture.png')


    page.click('//*[@id="weko-records"]/invenio-files-uploader/invenio-records/div[2]/div[8]/invenio-records-form/div/div/form/bootstrap-decorator[5]/fieldset/div/div[1]/a')

    page.press('//*[@id="weko-records"]/invenio-files-uploader/invenio-records/div[2]/div[8]/invenio-records-form/div/div/form/bootstrap-decorator[5]/fieldset/div/div[2]/div/div[1]/ol/li/sf-decorator/div/sf-decorator[1]/div/div/select', "ArrowDown")
                
    page.wait_for_timeout(int(SET_WAIT))
    
    page.screenshot(path=f'{"Autotest05_291_1"}_capture.png')

    #page.click('//*[@id="weko-records"]/invenio-files-uploader/invenio-records/div[2]/div[8]/invenio-records-form/div/div/form/bootstrap-decorator[6]/fieldset/div/div[1]/a')
    page.click("text=/.*Access Rights.*/")

    page.press('//*[@id="weko-records"]/invenio-files-uploader/invenio-records/div[2]/div[8]/invenio-records-form/div/div/form/bootstrap-decorator[6]/fieldset/div/div[2]/sf-decorator[1]/div/div/select', "ArrowDown")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{"Autotest05_295_1"}_capture.png')

    page.click('//*[@id="weko-records"]/invenio-files-uploader/invenio-records/div[2]/div[9]/div/div[1]/div/button[2]')

    page.wait_for_timeout(int(SET_WAIT))
    
    page.screenshot(path=f'{"Autotest05_296_1"}_capture.png')

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