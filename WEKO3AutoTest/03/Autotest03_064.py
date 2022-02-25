#from json import load
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

        # Click input[name="pubdate"]
    page.click("input[name=\"pubdate\"]")

    # Click text="02"
    page.click("text=\"02\"")

    #page.screenshot(path=f'{"Autotest03_043_1"}.png')

    # Fill input[name="item_1617186331708.0.subitem_1551255647225"]
    page.fill("input[name=\"item_1617186331708.0.subitem_1551255647225\"]", "登録テストアイテム1")

    # Click input[name="item_1617186331708.0.subitem_1551255647225"]
    page.click("input[name=\"item_1617186331708.0.subitem_1551255647225\"]")

    #page.screenshot(path=f'{"Autotest03_044_1"}.png')

    # Select string:ja
    page.select_option("//div[normalize-space(.)='jaja-Kanaenfritdeeszh-cnzh-twrulamseoarelko']/select", "string:ja")

    #page.screenshot(path=f'{"Autotest03_045_1"}.png')

    # Select string:conference paper
    page.select_option("//div[starts-with(normalize-space(.), 'conference paperdata paperdepartmental bulletin papereditorialjournal articlenew')]/select", "string:review article")
    # Resource Type が見える位置に画面を来させる為に、Version Typeをクリック
    page.click("//*[@id='weko-records']/invenio-files-uploader/invenio-records/div[2]/div[8]/invenio-records-form/div/div/form/bootstrap-decorator[17]/fieldset/div/div[1]/a")

    page.wait_for_timeout(int(SET_WAIT))
    page.screenshot(path=f'{path.splitext(path.basename(__file__))[0]+"_1"}.png')


    page.click('//*[@id="weko-records"]/invenio-files-uploader/invenio-records/div[2]/div[9]/div/div[1]/div/button[2]')

    page.wait_for_timeout(int(SET_WAIT)*2)
    
    #page.screenshot(path=f'{"Autotest03_055_1"}.png')

    # Check //div[normalize-space(.)='Index E(Embargo)']/div[2]/input[normalize-space(@type)='checkbox']
    page.check("//div[normalize-space(.)='Index E(Embargo)']/div[2]/input[normalize-space(@type)='checkbox']")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{path.splitext(path.basename(__file__))[0]+"_2"}.png')

    # Click text=/.*Next.*/
    page.click("text=/.*Next.*/")

    # Click textarea[id="input-comment"]
    page.click("textarea[id=\"input-comment\"]")

    # Fill textarea[id="input-comment"]
    page.fill("textarea[id=\"input-comment\"]", "AutoTest")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{path.splitext(path.basename(__file__))[0]+"_3"}.png')

    # Click text=/.*Next.*/
    page.click("text=/.*Next.*/")

    # Click //div[normalize-space(.)='Index C(No OAI-PMH)']/div[1]
    page.click("//div[normalize-space(.)='Index C(No OAI-PMH)']/div[1]")

    # Click text="Index C-1"
    page.click("text=\"Index C-1\"")

    page.wait_for_timeout(int(SET_WAIT))

    # Click text=/.*Next.*/
    page.click("text=/.*Next.*/")

    # Fill text=/.*JaLC DOI.*/ >> input[name="identifier_grant"]
    # page.fill("text=/.*JaLC DOI.*/ >> input[name=\"identifier_grant\"]", "1")

    # Click //td[normalize-space(.)='JaLC DOI']
    page.click("//td[normalize-space(.)='JaLC DOI']")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{path.splitext(path.basename(__file__))[0]+"_4"}.png')

    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)