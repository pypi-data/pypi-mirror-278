"""
    This class will start the test process
"""
from dataclasses import dataclass
from enum import Enum
from selenium.webdriver.chrome.webdriver import WebDriver
from ramda import path_or
from autotest.lib.lib.lend_event import LendEvent
from autotest.lib.runner.application_overview.runner import ApplicationOverviewTest
from autotest.lib.runner.application_workflow.runner import ApplicationWorkflowTest


class TestSource(Enum):
    """
    Hold the test types
    """
    APPLICATION_WORKFLOW = ApplicationWorkflowTest
    APPLICATION_OVERVIEW = ApplicationOverviewTest


@dataclass
class AutoTestInitializer:
    """
        This class will start the auto test based on test type
    """
    driver: WebDriver
    lend_event: LendEvent

    def __get_test_type(self):
        """
            This function returns the test type
        """
        return path_or("", ["event_data", "test_data", "test_type"], self.lend_event.event_data)

    def get_test_class(self):
        """
            Returns the test class
        """
        test_type = self.__get_test_type()
        test_class = getattr(TestSource, test_type).value
        return test_class

    def initailize(self):
        """
            Initialize the test
        """
        test_class_obj = self.get_test_class()
        return test_class_obj(
            driver=self.driver,
            data=path_or({}, ["event_data"], self.lend_event.event_data)
        ).run()
