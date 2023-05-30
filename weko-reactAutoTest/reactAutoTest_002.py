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
    if WEKO_URL.find('@'):
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
    styleClass = page.locator('//*[@id="id_' + CHECKBOX_NAME + '_chkbox"]/../../../div[2]').get_attribute('class')
    if styleClass.find('show') == -1:
        page.locator('//*[@id="id_' + CHECKBOX_NAME + '_chkbox"]/../../../div[1]/a').click()

    # Click on the checkbox for the FACET item.
    # Select 1
    queryValue1 = page.locator('//*[@id="id_' + CHECKBOX_NAME + '_chkbox_0"]').get_attribute('value')
    queryValueText = page.locator('//*[@id="id_' + CHECKBOX_NAME + '_chkbox_0"]/..').text_content()
    queryCount = queryValueText[queryValueText.rfind('(') + 1 :queryValueText.rfind(')')]

    page.locator('//*[@id="id_' + CHECKBOX_NAME + '_chkbox_0"]').check()
    page.screenshot(path=f'./Result/png/{"reactAutoTest_002_2-1_one_check"}_capture.png', full_page=True)
    page.wait_for_timeout(int(SET_WAIT))
    page.screenshot(path=f'./Result/png/{"reactAutoTest_002_2-1_one_count"}_capture.png', full_page=True)
    # After searching, check if the facet item value is included in the URL search criteria.
    params = urllib.parse.parse_qs(urllib.parse.urlparse(page.url).query)
    #params = urllib.parse.parse_qs(urllib.parse.unquote(urllib.parse.urlparse(page.url).query, 'shift-jis'))
    assert queryValue1 == params[CHECKBOX_NAME][0]

    # After the search, check the validity of the number of items.
    countContent = page.locator('ng-pluralize').text_content()
    count1 = countContent[countContent.rfind('of') + 2:countContent.rfind('results.')].strip()
    assert queryCount == count1

    # Select 2
    queryValue2 = page.locator('//*[@id="id_' + CHECKBOX_NAME + '_chkbox_1"]').get_attribute('value')
    page.locator('//*[@id="id_' + CHECKBOX_NAME + '_chkbox_1"]').check()
    page.screenshot(path=f'./Result/png/{"reactAutoTest_002_2-1_two_check"}_capture.png', full_page=True)
    page.wait_for_timeout(int(SET_WAIT))
    page.screenshot(path=f'./Result/png/{"reactAutoTest_002_2-1_two_count"}_capture.png', full_page=True)
    # After searching, check if the facet item value is included in the URL search criteria.
    params = urllib.parse.parse_qs(urllib.parse.urlparse(page.url).query)
    #params = urllib.parse.parse_qs(urllib.parse.unquote(urllib.parse.urlparse(page.url).query, 'shift-jis'))
    assert queryValue2 == params[CHECKBOX_NAME][1]

    # After the search, check the validity of the number of items.
    countContent = page.locator('ng-pluralize').text_content()
    count2 = countContent[countContent.rfind('of') + 2:countContent.rfind('results.')].strip()
    assert count2 != count1

    # Select-out 2
    page.locator('//*[@id="id_' + CHECKBOX_NAME + '_chkbox_1"]').uncheck()
    page.screenshot(path=f'./Result/png/{"reactAutoTest_002_2-2_two_check"}_capture.png', full_page=True)
    page.wait_for_timeout(int(SET_WAIT))
    page.screenshot(path=f'./Result/png/{"reactAutoTest_002_2-2_two_count"}_capture.png', full_page=True)
    params = urllib.parse.parse_qs(urllib.parse.urlparse(page.url).query)
    assert len(params[CHECKBOX_NAME]) == 1
    assert queryValue1 == params[CHECKBOX_NAME][0]

    # After the search, check the validity of the number of items.
    countContent = page.locator('ng-pluralize').text_content()
    count_out2 = countContent[countContent.rfind('of') + 2:countContent.rfind('results.')].strip()
    assert count_out2 == count1

    # Select-out 1
    page.locator('//*[@id="id_' + CHECKBOX_NAME + '_chkbox_0"]').uncheck()
    page.screenshot(path=f'./Result/png/{"reactAutoTest_002_2-2_one_check"}_capture.png', full_page=True)
    page.wait_for_timeout(int(SET_WAIT))
    page.screenshot(path=f'./Result/png/{"reactAutoTest_002_2-2_one_count"}_capture.png', full_page=True)
    params = urllib.parse.parse_qs(urllib.parse.urlparse(page.url).query)
    assert CHECKBOX_NAME not in params

    # After the search, check the validity of the number of items.
    countContent = page.locator('ng-pluralize').text_content()
    count_out1 = countContent[countContent.rfind('of') + 2:countContent.rfind('results.')].strip()
    assert count_out1 > count1
    
    # modal
    page.locator('//*[@id="id_' + CHECKBOX_NAME + '_chkbox"]/div/a').click()
    page.screenshot(path=f'./Result/png/{"reactAutoTest_002_2-3_modal"}_capture.png', full_page=True)

    modalStyleClass = page.locator('//*[@id="id_' + CHECKBOX_NAME + '_checkbox_modal"]').get_attribute('class')
    assert modalStyleClass.find('is-active') != -1

    # modal Select 1
    queryValueM1 = page.locator('//*[@id="id_' + CHECKBOX_NAME + '_chkbox_mdl_0"]').get_attribute('value')
    queryValueText = page.locator('//*[@id="id_' + CHECKBOX_NAME + '_chkbox_0"]/..').text_content()
    queryCount = queryValueText[queryValueText.rfind('(') + 1 :queryValueText.rfind(')')]

    page.locator('//*[@id="id_' + CHECKBOX_NAME + '_chkbox_mdl_0"]').check()
    page.screenshot(path=f'./Result/png/{"reactAutoTest_002_2-3_one_check"}_capture.png', full_page=True)
    page.locator('//*[@id="id_' + CHECKBOX_NAME + '_checkbox_modal"]/div/div/div[2]/button').click()
    page.wait_for_timeout(int(SET_WAIT))
    page.screenshot(path=f'./Result/png/{"reactAutoTest_002_2-3_one_count"}_capture.png', full_page=True)
    # After searching, check if the facet item value is included in the URL search criteria.
    params = urllib.parse.parse_qs(urllib.parse.urlparse(page.url).query)
    assert queryValueM1 == params[CHECKBOX_NAME][0]

    # After the search, check the validity of the number of items.
    countContent = page.locator('ng-pluralize').text_content()
    count1 = countContent[countContent.rfind('of') + 2:countContent.rfind('results.')].strip()
    assert queryCount == count1

    # modal Select 2
    page.locator('//*[@id="id_' + CHECKBOX_NAME + '_chkbox"]/div/a').click()

    queryValueM2 = page.locator('//*[@id="id_' + CHECKBOX_NAME + '_chkbox_mdl_1"]').get_attribute('value')
    page.locator('//*[@id="id_' + CHECKBOX_NAME + '_chkbox_mdl_1"]').check()
    page.screenshot(path=f'./Result/png/{"reactAutoTest_002_2-3_two_check"}_capture.png', full_page=True)
    page.locator('//*[@id="id_' + CHECKBOX_NAME + '_checkbox_modal"]/div/div/div[2]/button').click()
    page.wait_for_timeout(int(SET_WAIT))
    page.screenshot(path=f'./Result/png/{"reactAutoTest_002_2-3_two_count"}_capture.png', full_page=True)
    # After searching, check if the facet item value is included in the URL search criteria.
    params = urllib.parse.parse_qs(urllib.parse.urlparse(page.url).query)
    #params = urllib.parse.parse_qs(urllib.parse.unquote(urllib.parse.urlparse(page.url).query, 'shift-jis'))
    assert queryValueM2 == params[CHECKBOX_NAME][1]

    # After the search, check the validity of the number of items.
    countContent = page.locator('ng-pluralize').text_content()
    count2 = countContent[countContent.rfind('of') + 2:countContent.rfind('results.')].strip()
    assert count2 != count1

    # modal Select-out 2
    page.locator('//*[@id="id_' + CHECKBOX_NAME + '_chkbox"]/div/a').click()

    page.locator('//*[@id="id_' + CHECKBOX_NAME + '_chkbox_mdl_1"]').uncheck()
    page.screenshot(path=f'./Result/png/{"reactAutoTest_002_2-3_two_check_out"}_capture.png', full_page=True)
    page.locator('//*[@id="id_' + CHECKBOX_NAME + '_checkbox_modal"]/div/div/div[2]/button').click()
    page.wait_for_timeout(int(SET_WAIT))
    page.screenshot(path=f'./Result/png/{"reactAutoTest_002_2-3_two_out_count"}_capture.png', full_page=True)
    params = urllib.parse.parse_qs(urllib.parse.urlparse(page.url).query)
    assert len(params[CHECKBOX_NAME]) == 1
    assert queryValueM1 == params[CHECKBOX_NAME][0]

    # After the search, check the validity of the number of items.
    countContent = page.locator('ng-pluralize').text_content()
    count_out2 = countContent[countContent.rfind('of') + 2:countContent.rfind('results.')].strip()
    assert count_out2 == count1

    # modal Select-out 1
    page.locator('//*[@id="id_' + CHECKBOX_NAME + '_chkbox"]/div/a').click()

    page.locator('//*[@id="id_' + CHECKBOX_NAME + '_chkbox_mdl_0"]').uncheck()
    page.screenshot(path=f'./Result/png/{"reactAutoTest_002_2-3_one_check_out"}_capture.png', full_page=True)
    page.locator('//*[@id="id_' + CHECKBOX_NAME + '_checkbox_modal"]/div/div/div[2]/button').click()
    page.wait_for_timeout(int(SET_WAIT))
    page.screenshot(path=f'./Result/png/{"reactAutoTest_002_2-3_one_out_count"}_capture.png', full_page=True)
    params = urllib.parse.parse_qs(urllib.parse.urlparse(page.url).query)
    assert CHECKBOX_NAME not in params

    # After the search, check the validity of the number of items.
    countContent = page.locator('ng-pluralize').text_content()
    count_out1 = countContent[countContent.rfind('of') + 2:countContent.rfind('results.')].strip()
    assert count_out1 > count1

    # modal cancel
    page.locator('//*[@id="id_' + CHECKBOX_NAME + '_chkbox"]/div/a').click()
    page.screenshot(path=f'./Result/png/{"reactAutoTest_002_2-3_before_cancel"}_capture.png', full_page=True)
    page.locator('//*[@id="id_' + CHECKBOX_NAME + '_checkbox_modal"]/div/div/div[2]/a').click()
    page.screenshot(path=f'./Result/png/{"reactAutoTest_002_2-3_after_cancel"}_capture.png', full_page=True)
    modalStyleClass = page.locator('//*[@id="id_' + CHECKBOX_NAME + '_checkbox_modal"]').get_attribute('class')
    assert modalStyleClass.find('is-active') == -1

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