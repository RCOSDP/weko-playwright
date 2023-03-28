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
    styleClass = page.locator('//*[@id="id_' + RANGESLIDER_NAME + '_slider"]/../../../div[2]').get_attribute('class')
    if styleClass.find('show') == -1:
        page.locator('//*[@id="id_' + RANGESLIDER_NAME + '_slider"]/../../../div[1]/a').click()

    element_from = page.locator('//*[@id="id_' + RANGESLIDER_NAME + '_slider_input_head"]')
    element_to = page.locator('//*[@id="id_' + RANGESLIDER_NAME + '_slider_input_tail"]')

    base_value_from = element_from.get_attribute('value')
    base_value_to = element_to.get_attribute('value')
    
    leftSlider = page.locator('//*[@id="id_' + RANGESLIDER_NAME + '_slider"]').locator('.rc-slider-handle-1')
    slider = page.locator('//*[@id="id_' + RANGESLIDER_NAME + '_slider"]').locator('.rc-slider')
    leftSlider.scroll_into_view_if_needed()

    startX = leftSlider.bounding_box()['x'] + leftSlider.bounding_box()['width'] / 2
    startY = leftSlider.bounding_box()['y'] + leftSlider.bounding_box()['height'] / 2
    endX = startX + slider.bounding_box()['width'] / 4
    endY = startY

    page.mouse.move(startX, startY)
    page.mouse.down()
    page.mouse.move(endX, endY)
    page.mouse.up()
    page.screenshot(path=f'./Result/png/{"reactAutoTest_003_3-1_left"}_capture.png', full_page=True)
    element_from = page.locator('//*[@id="id_' + RANGESLIDER_NAME + '_slider_input_head"]')
    changed_value_from = element_from.get_attribute('value')
    assert base_value_from < changed_value_from

    rightSlider = page.locator('//*[@id="id_' + RANGESLIDER_NAME + '_slider"]').locator('.rc-slider-handle-2')
    rightSlider.scroll_into_view_if_needed()
    startX = rightSlider.bounding_box()['x'] + rightSlider.bounding_box()['width'] / 2
    startY = rightSlider.bounding_box()['y'] + rightSlider.bounding_box()['height'] / 2
    endX = startX - slider.bounding_box()['width'] / 4
    endY = startY

    page.mouse.move(startX, startY)
    page.mouse.down()
    page.mouse.move(endX, endY)
    page.mouse.up()
    page.screenshot(path=f'./Result/png/{"reactAutoTest_003_3-1_right"}_capture.png', full_page=True)
    element_to = page.locator('//*[@id="id_' + RANGESLIDER_NAME + '_slider_input_tail"]')
    changed_value_to = element_to.get_attribute('value')
    assert base_value_to > changed_value_to

    range_from = element_from.get_attribute('value')
    range_to = element_to.get_attribute('value')
    queryValue = range_from + '--'+ range_to

    page.locator('//*[@id="id_' + RANGESLIDER_NAME + '_slider"]').locator('button').click()
    page.wait_for_timeout(int(SET_WAIT))
    page.screenshot(path=f'./Result/png/{"reactAutoTest_003_3-5"}_capture.png', full_page=True)

    # After searching, check if the facet item value is included in the URL search criteria.
    params = urllib.parse.parse_qs(urllib.parse.urlparse(page.url).query)
    assert queryValue == params[RANGESLIDER_NAME][0]

    element_from.fill('')
    page.locator('//*[@id="id_' + RANGESLIDER_NAME + '_slider"]').locator('button').click()
    page.screenshot(path=f'./Result/png/{"reactAutoTest_003_3-2_left"}_capture.png', full_page=True)
    element_from = page.locator('//*[@id="id_' + RANGESLIDER_NAME + '_slider_input_head"]')
    element_to = page.locator('//*[@id="id_' + RANGESLIDER_NAME + '_slider_input_tail"]')
    assert element_from.get_attribute('class').find('range-slider-error') != -1
    assert element_to.get_attribute('class').find('range-slider-error') == -1
    element_from.fill(range_from)

    element_to.fill('')
    page.locator('//*[@id="id_' + RANGESLIDER_NAME + '_slider"]').locator('button').click()
    page.screenshot(path=f'./Result/png/{"reactAutoTest_003_3-2_right"}_capture.png', full_page=True)
    element_from = page.locator('//*[@id="id_' + RANGESLIDER_NAME + '_slider_input_head"]')
    element_to = page.locator('//*[@id="id_' + RANGESLIDER_NAME + '_slider_input_tail"]')
    assert element_from.get_attribute('class').find('range-slider-error') == -1
    assert element_to.get_attribute('class').find('range-slider-error') != -1
    element_to.fill(range_to)

    element_from.fill('-123')
    page.locator('//*[@id="id_' + RANGESLIDER_NAME + '_slider"]').locator('button').click()
    page.screenshot(path=f'./Result/png/{"reactAutoTest_003_3-3_left"}_capture.png', full_page=True)
    element_from = page.locator('//*[@id="id_' + RANGESLIDER_NAME + '_slider_input_head"]')
    element_to = page.locator('//*[@id="id_' + RANGESLIDER_NAME + '_slider_input_tail"]')
    assert element_from.get_attribute('class').find('range-slider-error') != -1
    assert element_to.get_attribute('class').find('range-slider-error') == -1
    element_from.fill(range_from)

    element_to.fill('-123')
    page.locator('//*[@id="id_' + RANGESLIDER_NAME + '_slider"]').locator('button').click()
    page.screenshot(path=f'./Result/png/{"reactAutoTest_003_3-3_right"}_capture.png', full_page=True)
    element_from = page.locator('//*[@id="id_' + RANGESLIDER_NAME + '_slider_input_head"]')
    element_to = page.locator('//*[@id="id_' + RANGESLIDER_NAME + '_slider_input_tail"]')
    assert element_from.get_attribute('class').find('range-slider-error') == -1
    assert element_to.get_attribute('class').find('range-slider-error') != -1
    element_to.fill(range_to)

    element_from.fill(range_to)
    element_to.fill(range_from)
    page.locator('//*[@id="id_' + RANGESLIDER_NAME + '_slider"]').locator('button').click()
    page.screenshot(path=f'./Result/png/{"reactAutoTest_003_3-4"}_capture.png', full_page=True)
    element_from = page.locator('//*[@id="id_' + RANGESLIDER_NAME + '_slider_input_head"]')
    element_to = page.locator('//*[@id="id_' + RANGESLIDER_NAME + '_slider_input_tail"]')
    assert element_from.get_attribute('class').find('range-slider-error') != -1
    assert element_to.get_attribute('class').find('range-slider-error') != -1
    element_from.fill(range_from)
    element_to.fill(range_to)



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