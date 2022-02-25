#from json import load
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

    # Click text=/.*Click to select.*/
    with page.expect_file_chooser() as fc_info:
        page.click("text=/.*Click to select.*/")
    file_chooser = fc_info.value
    file_chooser.set_files("sample.pdf")

    page.screenshot(path=f'{"Autotest03_001_1"}.png')

    # Click text="Start upload"
    page.click("text=\"Start upload\"")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{"Autotest03_007_1"}.png')

    # Click text=/.*Click to select.*/
    with page.expect_file_chooser() as fc_info:
        page.click("text=/.*Click to select.*/")
    file_chooser = fc_info.value
    file_chooser.set_files("sample.pptx")

    # Click text="Start upload"
    page.click("text=\"Start upload\"")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{"Autotest03_009_1"}.png')

    # Click text=/.*Click to select.*/
    with page.expect_file_chooser() as fc_info:
        page.click("text=/.*Click to select.*/")
    file_chooser = fc_info.value
    file_chooser.set_files("sample.docx")

    # Click text="Start upload"
    page.click("text=\"Start upload\"")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{"Autotest03_011_1"}.png')

    # Click text=/.*Click to select.*/
    with page.expect_file_chooser() as fc_info:
        page.click("text=/.*Click to select.*/")
    file_chooser = fc_info.value
    file_chooser.set_files("sample.xlsx")

    # Click text="Start upload"
    page.click("text=\"Start upload\"")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{"Autotest03_013_1"}.png')

    # Click text=/.*Click to select.*/
    with page.expect_file_chooser() as fc_info:
        page.click("text=/.*Click to select.*/")
    file_chooser = fc_info.value
    file_chooser.set_files("sample.txt")

    # Click text="Start upload"
    page.click("text=\"Start upload\"")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{"Autotest03_015_1"}.png')

    # Click text=/.*Click to select.*/
    with page.expect_file_chooser() as fc_info:
        page.click("text=/.*Click to select.*/")
    file_chooser = fc_info.value
    file_chooser.set_files("sample.mpeg")

    # Click text="Start upload"
    page.click("text=\"Start upload\"")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{"Autotest03_017_1"}.png')

    # Click text=/.*Click to select.*/
    with page.expect_file_chooser() as fc_info:
        page.click("text=/.*Click to select.*/")
    file_chooser = fc_info.value
    file_chooser.set_files("sample.swf")

    # Click text="Start upload"
    page.click("text=\"Start upload\"")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{"Autotest03_019_1"}.png')

    # Click text=/.*Click to select.*/
    with page.expect_file_chooser() as fc_info:
        page.click("text=/.*Click to select.*/")
    file_chooser = fc_info.value
    file_chooser.set_files("sample.mp3")

    # Click text="Start upload"
    page.click("text=\"Start upload\"")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{"Autotest03_021_1"}.png')

    # Click text=/.*Click to select.*/
    with page.expect_file_chooser() as fc_info:
        page.click("text=/.*Click to select.*/")
    file_chooser = fc_info.value
    file_chooser.set_files("sample.png")

    # Click text="Start upload"
    page.click("text=\"Start upload\"")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{"Autotest03_023_1"}.png')
    
    # Click text=/.*Click to select.*/
    with page.expect_file_chooser() as fc_info:
        page.click("text=/.*Click to select.*/")
    file_chooser = fc_info.value
    file_chooser.set_files("sample.png")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{"Autotest03_024_1"}.png')

    # Click div[id="step_page"] div[role="document"] >> text=/.*Cancel.*/
    page.click("div[id=\"step_page\"] div[role=\"document\"] >> text=/.*Cancel.*/")

    # Click //tr[normalize-space(.)='sample.png ... 28 Kb 100 % Processing... Error ']/td[4]/a/i
    # with page.expect_navigation(url="https://localhost/workflow/activity/detail/A-20220203-00001"):
    # with page.expect_navigation():
    # page.click("//tr[normalize-space(.)='sample.pdf ... 43 Kb 100 % Processing... Error ']/td[4]/a/i")
    page.click('//*[@id="file_upload"]/div/invenio-files-list/div/table/tbody/tr[2]/td[4]/a/i')
    #//*[@id="file_upload"]/div/invenio-files-list/div/table/tbody/tr[2]

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{"Autotest03_025_1"}.png')

        # Click input[name="pubdate"]
    page.click("input[name=\"pubdate\"]")

    # Click text="02"
    page.click("text=\"02\"")

    page.screenshot(path=f'{"Autotest03_043_1"}.png')

    # Fill input[name="item_1617186331708.0.subitem_1551255647225"]
    page.fill("input[name=\"item_1617186331708.0.subitem_1551255647225\"]", "登録テストアイテム1")

    # Click input[name="item_1617186331708.0.subitem_1551255647225"]
    page.click("input[name=\"item_1617186331708.0.subitem_1551255647225\"]")

    page.screenshot(path=f'{"Autotest03_044_1"}.png')

    # Select string:ja
    page.select_option("//div[normalize-space(.)='jaja-Kanaenfritdeeszh-cnzh-twrulamseoarelko']/select", "string:ja")

    page.screenshot(path=f'{"Autotest03_045_1"}.png')

    # Select string:conference paper
    page.select_option("//div[starts-with(normalize-space(.), 'conference paperdata paperdepartmental bulletin papereditorialjournal articlenew')]/select", "string:conference paper")
    # Resource Type が見える位置に画面を来させる為に、Version Typeをクリック
    page.click("//*[@id='weko-records']/invenio-files-uploader/invenio-records/div[2]/div[8]/invenio-records-form/div/div/form/bootstrap-decorator[17]/fieldset/div/div[1]/a")

    page.wait_for_timeout(int(SET_WAIT))
    page.screenshot(path=f'{"Autotest03_046_1"}.png')

    # Click text="Input from author DB"
    page.click("text=\"Input from author DB\"")

    page.wait_for_timeout(int(SET_WAIT))

    page.fill("//html/body/div[3]/div[2]/div/div/div[1]/div/div/div/div/div[1]/div/div[1]/input", "情報")

    #page1.click('button.btn.btn-primary.search-button')
    page.click("//html/body/div[3]/div[2]/div/div/div[1]/div/div/div/div/div[1]/div/div[2]/button")

    page.click('//*[@id="table_data"]/tbody/tr/td[3]/button')

    page.click('//html/body/div[3]/div[2]/div/div/div[2]/button')

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{"Autotest03_052_1"}.png')

    page.click('//*[@id="weko-records"]/invenio-files-uploader/invenio-records/div[2]/div[9]/div/div[1]/div/button[2]')

    page.wait_for_timeout(int(SET_WAIT))
    page.wait_for_timeout(int(SET_WAIT))
    
    page.screenshot(path=f'{"Autotest03_055_1"}.png')

    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)