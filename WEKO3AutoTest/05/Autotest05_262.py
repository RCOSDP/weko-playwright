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

    # Click text=/.*Click to select.*/
    with page.expect_file_chooser() as fc_info:
        page.click("text=/.*Click to select.*/")
    file_chooser = fc_info.value
    file_chooser.set_files("sample.pdf")

    page.wait_for_timeout(int(SET_WAIT))

    # Click text="Start upload"
    page.click("text=\"Start upload\"")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{path.splitext(path.basename(__file__))[0]+"_1"}_capture.png')


    # Click input[name="pubdate"]
    page.click("input[name=\"pubdate\"]")

    # Click text="02"
    page.click("text=\"02\"")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{path.splitext(path.basename(__file__))[0]+"_2"}_capture.png')

    # Fill input[name="item_1617186331708.0.subitem_1551255647225"]
    page.fill("input[name=\"item_1617186331708.0.subitem_1551255647225\"]", "登録テストアイテム（ユーザマニュアル）")


    page.screenshot(path=f'{"Autotest05_263_1"}_capture.png')

    # Select string:ja
    page.select_option("//div[normalize-space(.)='jaja-Kanaenfritdeeszh-cnzh-twrulamseoarelko']/select", "string:ja")

    page.screenshot(path=f'{"Autotest05_264_1"}_capture.png')

    # Click //a[normalize-space(.)='File']/span[1]/i
    page.click('//*[@id="weko-records"]/invenio-files-uploader/invenio-records/div[2]/div[8]/invenio-records-form/div/div/form/bootstrap-decorator[1]/fieldset/div/div[1]/a')
                
    # Click //a[normalize-space(.)='Text URL']/span[1]/i
    page.click('//*[@id="weko-records"]/invenio-files-uploader/invenio-records/div[2]/div[8]/invenio-records-form/div/div/form/bootstrap-decorator[1]/fieldset/div/div[2]/div/div[1]/ol/li[1]/sf-decorator/div/sf-decorator[2]/fieldset/div/div[1]/a')

    page.select_option("//div[normalize-space(.)='abstractsummaryfulltextthumbnailother']/select", "string:abstract")

    page.wait_for_timeout(int(SET_WAIT))
    page.screenshot(path=f'{"Autotest05_265_1"}_capture.png')

    # Click text=/.*Creator.*/
    page.click("text=/.*Creator.*/")

    # Click text=/.*著者DBから入力.*/
    page.click("text=/.*著者DBから入力.*/")

    page.wait_for_timeout(int(SET_WAIT))
   
    # page.fill("div[role=\"document\"] input[type=\"text\"]", "情報")
    page.fill("//*[@id='app-author-search']/div/div/div[1]/app-author-search/div/div/div/div/div[2]/div[1]/input", "情報")

    page.click("//*[@id='app-author-search']/div/div/div[1]/app-author-search/div/div/div/div/div[2]/div[2]/button")

    page.click('//*[@id="input_button_0"]')

    page.wait_for_timeout(int(SET_WAIT))

    page.click("text=/.*Creator Identifier.*/")
    
    page.wait_for_timeout(int(SET_WAIT))
    
    page.screenshot(path=f'{"Autotest05_278_1"}_capture.png')

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