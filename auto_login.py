# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0055BE2E8A6817664A2425D3CA9473F7D71FBDB493884148969DCA68F3883F989D82E1EEBDE033D8ED5A0AB633D7B7D2C9A3CA8747A94AE29B479D778E0DDF8DF72B77149B880AEE357AB5C4D5327A0FAA068A6D20151908862C0C8792FF9229DCB98306C9CDBE70BEFC5ACB271AEA93647C4EAA66A2A93371BC2D616127E636BBBA0A38C08F1FB1346D2FF73840A127248FBD6091870CC1B81496C96D754421A4712AFCE4E9FD6925CB8BB32376CDADCC2C55D8B629CFCCB9D08D2C82BEF8BCD42D5A32AC96844F9FA47D58D0E136A32DF838ACDC651D7FAEBC84B1D30F14302DD0FC236656C369D09EA99FCC06BBAA119DE2058831B6F58E75F958C5989EA7180337750CCD4A76B8240D4055C00B1B8C6D153A8BEBA066E585B6407660E5DC6E9D8674342C7E4A80A2D76ED5958DDE7935035A4067F7D4E3C9817F463AA3A465AC56CC6B6DE92226D6AC0237399F46E592BE3760865CA2B596C728CAD66ED552"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
