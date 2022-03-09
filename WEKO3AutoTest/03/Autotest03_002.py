import pytest
import configparser
from playwright.sync_api import sync_playwright

config_ini = configparser.ConfigParser()
config_ini.read( "conf.ini", encoding = "utf-8" )
print("SET_TIMEOUT = " + config_ini['DEFAULT']['SETTIMEOUT'])
print("SET_WAIT = " + config_ini['DEFAULT']['SETWAIT'])
SET_TIMEOUT = config_ini['DEFAULT']['SETTIMEOUT']
SET_WAIT = config_ini['DEFAULT']['SETWAIT']

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

    # Click input[name="email"]
    # page.click("input[name=\"email\"]")

    # Fill input[name="email"]
    page.fill("input[name=\"email\"]", "wekosoftware@nii.ac.jp")

    # Click input[name="password"]
    # page.click("input[name=\"password\"]")

    # Fill input[name="password"]
    page.fill("input[name=\"password\"]", "uspass123")

    # Click text=/.*Log In.*/
    page.click("text=/.*Log In.*/")
    # assert page.url == "https://localhost/"

    # Click text="Workflow"
    page.click("text=\"Workflow\"")
    # assert page.url == "https://localhost/workflow/"

    # Click text=/.*New Activity.*/
    # page.click("text=/.*New Activity.*/")
    # assert page.url == "https://localhost/workflow/activity/new"

    # Click text=/.*New.*/
    # page.click("text=/.*New.*/")

    # Go to https://localhost/workflow/activity/detail/A-20220203-00001
    page.goto("https://localhost/workflow/activity/detail/A-20220203-00002",timeout=int(SET_TIMEOUT))
    # page.wait_for_timeout(5000)

    # Click div[id="activity_locked"] >> text="OK"
    page.click("div[id=\"activity_locked\"] >> text=\"OK\"")

    #/html/body/div[3]/div[2]/div/div/div[1]/div/div/div/div/div[1]/div/div[2]/button
    # Click text="Input from author DB"
    #with page.expect_popup(predicate = page ) as popup_info:
    page.click("text=\"Input from author DB\"")
    #page1 = popup_info.value
    #page1.wait_for_timeout(int(SET_WAIT))
    #page1.full("//div/html/body/div[3]/div[2]/div/div/div[1]/div/div/div/div/div[1]/div/div[1]/input/div[1]/input", "亀田")

    #page1.wait_for_timeout(int(SET_WAIT))

    page.fill("//html/body/div[3]/div[2]/div/div/div[1]/div/div/div/div/div[1]/div/div[1]/input", "亀田")

    #page1.click('button.btn.btn-primary.search-button')
    page.click("//html/body/div[3]/div[2]/div/div/div[1]/div/div/div/div/div[1]/div/div[2]/button")

    page.click('//*[@id="table_data"]/tbody/tr/td[3]/button')

    page.click('//html/body/div[3]/div[2]/div/div/div[2]/button')

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{"Autotest03_048_1"}_capture.png')

    #page1.close()

    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)