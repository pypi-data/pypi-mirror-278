"""
    setup the driver
"""
# pylint:disable=C0415,E0401,R0903
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class DriverSetup:
    """
    Setup the driver
    """

    def get_driver(
        self, browser_type: str, driver_path: str = None, chromium_path: str = None
    ):
        """
        load the driver
        """
        driver = None
        if not driver_path:
            driver_path = "/opt/chromedriver"
        if not chromium_path:
            chromium_path = "/opt/chrome/chrome"
        print("driver path==>", driver_path)

        from urllib3.connectionpool import log as urllibLogger

        urllibLogger.setLevel(logging.INFO)

        if browser_type == "headless-chromium": 
            #loadBrowser(browser_driver=["headless-chromium","chromedriver"])
            options = Options()
            options.binary_location = chromium_path
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--single-process')
            options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(driver_path,chrome_options=options)
            driver.maximize_window()

        print(driver.get_window_size())
        return driver
