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

    # Click //div[normalize-space(.)='Index A']/div[1]
    page.click("//*[@id='index-background']/app-tree-items/app-tree-list2/div/div/div/tree/tree-internal/ul/li/tree-internal[1]/ul/li/div/div[2]/span")

    # Click text="Index A-1"
    # with page.expect_navigation(url="https://localhost/search?page=1&size=20&sort=controlnumber&timestamp=1645775555.2401288&search_type=2&q=1029&time=1645775554713"):
    #with page.expect_navigation():
        #page.click("text=\"Index A-1\"")

    # Click text="title"        
    #　page.click("//*[@id='index_item_list']/div[2]/div/div/invenio-search-results/div/div[1]/div/a")
    page.click("//*[@id='index_item_list']/div[2]/div/div/invenio-search-results/div[10]/div[1]/div/a")
                
    # assert page.url == "https://localhost/records/301"

    page.wait_for_timeout(int(SET_WAIT)*2)

    page.screenshot(path=f'{path.splitext(path.basename(__file__))[0]+"_1"}.png')

    page.wait_for_timeout(int(SET_WAIT))

    # Click text=/.*Edit.*/
    page.click("//*[@id='btn_delete']")

    page.wait_for_timeout(int(SET_WAIT)*2)
    
    # assert page.url == "https://localhost/records/301#/!"
    page.screenshot(path=f'{path.splitext(path.basename(__file__))[0]+"_2"}.png')

    # Click text = OK 
    page.click("//html/body/div[5]/div/div/div[3]/button[1]")

    page.wait_for_timeout(int(SET_WAIT))

    page.screenshot(path=f'{path.splitext(path.basename(__file__))[0]+"_3"}.png')

    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)