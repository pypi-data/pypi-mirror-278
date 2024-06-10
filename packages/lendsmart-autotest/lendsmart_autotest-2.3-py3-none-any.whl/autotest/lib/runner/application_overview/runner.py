"""
    overview tester
"""
from dataclasses import dataclass
from selenium.webdriver.chrome.webdriver import WebDriver


@dataclass
class ApplicationOverviewTest:
    """
        test the overview
    """
    driver: WebDriver
    data: dict

    def run(self):
        """
            This function eill 
        """
