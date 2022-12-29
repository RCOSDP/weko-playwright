__file__
import pytest
import configparser
from playwright.sync_api import sync_playwright

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

def test_issue35133():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(ignore_https_errors=True)
        
        # Open new page
        page = context.new_page()
        
        # Go to https://localhost/
        page.goto(WEKO_URL)
        
        # Click detail_searc
        page.click('//*[@id="detail_search_main"]')

        # Scroll to index checkbox_list
        index_checkbox = page.locator('//div[@class="content_21"]')
        index_checkbox.scroll_into_view_if_needed()
        page.screenshot(path="imgs/1_capture.png")
        
        index_checkbox_labels = page.locator('//div[@class="content_21"]/label')
        index_count = index_checkbox_labels.count()
        if index_count == 50:
            # the number of indexes is 50 or more
            
            box = index_checkbox.bounding_box()
            assert box["height"] == 400
            
            # Scroll above index checkbox
            page.mouse.move(box["x"]+(box["width"]/2),box["y"])
            page.mouse.wheel(0,460)
            page.screenshot(path="imgs/2_capture.png")
            index_count2 = index_checkbox_labels.count()
            assert index_count2 > 50
        else:
            pass
        page.close()
        
        context.close()
        browser.close()