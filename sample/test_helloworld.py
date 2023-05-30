import pytest
from playwright.sync_api import Browser, BrowserType


def test_helloworld(browser: Browser, browser_type: BrowserType):
    page = browser.new_page(
        record_video_dir='videos/', record_video_size={
            "width": 640, "height": 480}
    )
    page.goto('https://www.google.co.jp/')
    page.fill('input[name=q]', 'RCOS')
    with page.expect_navigation():
        page.click('input[name=btnK]')
    page.screenshot(path=f'images/{browser_type.name}.png')
    page.wait_for_timeout(1000)
    text = page.text_content(
        '//*[@id="rso"]/div[1]/div/div/div/div/div/div/div/div[1]/a/h3')
    assert text == '国立情報学研究所 オープンサイエンス基盤研究センター'
    page.context.close()
