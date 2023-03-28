__file__
import configparser
import urllib.parse
from playwright.sync_api import sync_playwright
from distutils.util import strtobool

config_ini = configparser.ConfigParser()
config_ini.read( "conf.ini", encoding = "utf-8" )

SET_TIMEOUT = config_ini['DEFAULT']['SETTIMEOUT']
SET_WAIT = config_ini['DEFAULT']['SETWAIT']
CHECKBOX_NAME = config_ini['DEFAULT']['CHECKBOX']
SELECTBOX_NAME = config_ini['DEFAULT']['SELECTBOX']
RANGESLIDER_NAME = config_ini['DEFAULT']['RANGESLIDER']
WEKO_URL = config_ini['DEFAULT']['WEKOURL']
WEKO_URL2 = config_ini['DEFAULT']['WEKOURL2']
ALL_SELECT_TEST = config_ini['DEFAULT']['ALLSELECTTEST']
ENGLISH_MODE = config_ini['DEFAULT']['ENGLISHMODE']
print("SET_TIMEOUT = " + SET_TIMEOUT)
print("SET_WAIT = " + SET_WAIT)
print("CHECKBOX_NAME = " + CHECKBOX_NAME)
print("SELECTBOX_NAME = " + SELECTBOX_NAME)
print("RANGESLIDER_NAME = " + RANGESLIDER_NAME)
print("WEKO_URL = " + WEKO_URL)
print("ALL_SELECT_TEST = " + ALL_SELECT_TEST)

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(ignore_https_errors=True)

    # Open new page
    page = context.new_page()

    # Go to
    page.goto(WEKO_URL,timeout=int(SET_TIMEOUT))
    page.wait_for_timeout(int(SET_WAIT))

    # If the URL includes basic authentication for CORS measures, reload the URL with no basic authentication.
    if WEKO_URL.find('@') != -1:
        page.goto(WEKO_URL2,timeout=int(SET_TIMEOUT))
        page.wait_for_timeout(int(SET_WAIT))

    # To test in English, change the language to English.
    if strtobool(ENGLISH_MODE):
        page.locator('#lang-code').select_option('English')
        page.wait_for_timeout(int(SET_WAIT))

    # Obtains a snapshot of the initial state.
    page.screenshot(path=f'./Result/png/{"reactAutoTest_001"}_capture.png', full_page=True)
    
    # Open FACET item column
    # If the facet item column is closed, it will open.
    styleClass = page.locator('//*[@id="id_' + SELECTBOX_NAME + '_select"]/../../../div[2]').get_attribute('class')
    if styleClass.find('show') == -1:
        page.locator('//*[@id="id_' + SELECTBOX_NAME + '_select"]/../../../div[1]/a').click()

    # Open SelectBox
    page.locator('//*[@id="id_' + SELECTBOX_NAME + '_select"]/div/div/div[1]/div[2]').locator('svg').click()
    page.screenshot(path=f'./Result/png/{"reactAutoTest_001_1-1"}_capture.png', full_page=True)

    # Click on the selectbox for the FACET item.
    # Select 1
    # The multi-select UI popup may close after the screenshot is taken; if it does, reopen it.
    styleClass = page.locator('//*[@id="id_' + SELECTBOX_NAME + '_select"]/div/div/div[1]').get_attribute('class')
    if styleClass.find('menu-is-open') == -1:
        page.locator('//*[@id="id_' + SELECTBOX_NAME + '_select"]/div/div/div[1]/div[2]').locator('svg').click()

    queryValueText = page.locator('//*[@id="id_' + SELECTBOX_NAME + '_select"]/div/div/div[2]/div[1]/div[1]').text_content()
    queryValue1 = queryValueText[0:queryValueText.rfind('(')]
    queryCount = queryValueText[queryValueText.rfind('(') + 1 :queryValueText.rfind(')')]

    page.locator('//*[@id="id_' + SELECTBOX_NAME + '_select"]/div/div/div[2]/div[1]/div[1]').click()
    page.screenshot(path=f'./Result/png/{"reactAutoTest_001_1-2_one_check"}_capture.png', full_page=True)
    page.wait_for_timeout(int(SET_WAIT))
    page.screenshot(path=f'./Result/png/{"reactAutoTest_001_1-2_one_count"}_capture.png', full_page=True)
    # After searching, check if the facet item value is included in the URL search criteria.
    params = urllib.parse.parse_qs(urllib.parse.urlparse(page.url).query)
    assert queryValue1 == params[SELECTBOX_NAME][0]
    # After the search, check the validity of the number of items.
    countContent = page.locator('ng-pluralize').text_content()
    count1 = countContent[countContent.rfind('of') + 2:countContent.rfind('results.')].strip()
    assert queryCount == count1

    # Select 2
    page.locator('//*[@id="id_' + SELECTBOX_NAME + '_select"]/div/div/div[1]/div[2]').locator('svg').click()
    queryValueText = page.locator('//*[@id="id_' + SELECTBOX_NAME + '_select"]/div/div/div[2]/div[1]/div[1]').text_content()
    queryValue2 = queryValueText[0:queryValueText.rfind('(')]

    page.locator('//*[@id="id_' + SELECTBOX_NAME + '_select"]/div/div/div[2]/div[1]/div[1]').click()
    page.screenshot(path=f'./Result/png/{"reactAutoTest_001_1-2_two_check"}_capture.png', full_page=True)
    page.wait_for_timeout(int(SET_WAIT))
    page.screenshot(path=f'./Result/png/{"reactAutoTest_001_1-2_two_count"}_capture.png', full_page=True)
    # After searching, check if the facet item value is included in the URL search criteria.
    params = urllib.parse.parse_qs(urllib.parse.urlparse(page.url).query)
    assert queryValue2 == params[SELECTBOX_NAME][1]
    # After the search, check the validity of the number of items.
    countContent = page.locator('ng-pluralize').text_content()
    count2 = countContent[countContent.rfind('of') + 2:countContent.rfind('results.')].strip()
    assert count2 != count1

    # If the test of all cases is targeted for implementation, the test of all cases is performed.
    if strtobool(ALL_SELECT_TEST):
        # Select All
        page.locator('//*[@id="id_' + SELECTBOX_NAME + '_select"]/div/div/div[1]/div[2]').locator('svg').click()
        elementList = page.locator('//*[@id="id_' + SELECTBOX_NAME + '_select"]/div/div/div[2]/div[1]/div').all()
        for i in range(len(elementList)):
            page.locator('//*[@id="id_' + SELECTBOX_NAME + '_select"]/div/div/div[2]/div[1]/div[1]').click()
            page.wait_for_timeout(int(SET_WAIT))
            page.locator('//*[@id="id_' + SELECTBOX_NAME + '_select"]/div/div/div[1]/div[2]').locator('svg').click()

        page.screenshot(path=f'./Result/png/{"reactAutoTest_001_1-2_all_count"}_capture.png', full_page=True)

        # Select All - out
        for i in range(len(elementList)):
            targetIndex = i + 2
            page.locator('//*[@id="id_' + SELECTBOX_NAME + '_select"]/div/div/div[1]/div[1]/div[' + str(targetIndex) +']').locator('svg').click()
            page.wait_for_timeout(int(SET_WAIT))
            page.locator('//*[@id="id_' + SELECTBOX_NAME + '_select"]/div/div/div[1]/div[2]').locator('svg').click()
            
        page.screenshot(path=f'./Result/png/{"reactAutoTest_001_1-3_all_check_out"}_capture.png', full_page=True)
        page.screenshot(path=f'./Result/png/{"reactAutoTest_001_1-3_all_out_count"}_capture.png', full_page=True)

    # Select 2 - out
    page.locator('//*[@id="id_' + SELECTBOX_NAME + '_select"]/div/div/div[1]/div[1]/div[2]').locator('svg').click()
    page.screenshot(path=f'./Result/png/{"reactAutoTest_001_1-3_two_check_out"}_capture.png', full_page=True)
    page.wait_for_timeout(int(SET_WAIT))
    page.screenshot(path=f'./Result/png/{"reactAutoTest_001_1-3_two_out_count"}_capture.png', full_page=True)
    # After the search, check the validity of the number of items.
    countContent = page.locator('ng-pluralize').text_content()
    count_out2 = countContent[countContent.rfind('of') + 2:countContent.rfind('results.')].strip()
    assert count_out2 == count1

    # Select 1 - out
    page.locator('//*[@id="id_' + SELECTBOX_NAME + '_select"]/div/div/div[1]/div[1]/div[1]').locator('svg').click()
    page.screenshot(path=f'./Result/png/{"reactAutoTest_001_1-3_one_check_out"}_capture.png', full_page=True)
    page.wait_for_timeout(int(SET_WAIT))
    page.screenshot(path=f'./Result/png/{"reactAutoTest_001_1-3_one_out_count"}_capture.png', full_page=True)
    # After the search, check the validity of the number of items.
    countContent = page.locator('ng-pluralize').text_content()
    count_out1 = countContent[countContent.rfind('of') + 2:countContent.rfind('results.')].strip()
    assert count_out1 > count1
    
    page.locator('//*[@id="id_' + SELECTBOX_NAME + '_select"]/div/div/div[1]').locator('input').fill("metadata")
    valueText = page.locator('//*[@id="id_' + SELECTBOX_NAME + '_select"]/div/div/div[2]/div[1]/div[1]').text_content()
    value = valueText[0:valueText.rfind('(')]
    assert value.find('metadata') != -1
    page.screenshot(path=f'./Result/png/{"reactAutoTest_001_1-4_data"}_capture.png', full_page=True)

    page.locator('//*[@id="id_' + SELECTBOX_NAME + '_select"]/div/div/div[1]').locator('input').fill("dummy")
    valueText = page.locator('//*[@id="id_' + SELECTBOX_NAME + '_select"]/div/div/div[2]/div[1]/div[1]').text_content()
    value = valueText[0:valueText.rfind('(')]
    assert value.find('dummy') == -1
    page.screenshot(path=f'./Result/png/{"reactAutoTest_001_1-4_nodata"}_capture.png', full_page=True)


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