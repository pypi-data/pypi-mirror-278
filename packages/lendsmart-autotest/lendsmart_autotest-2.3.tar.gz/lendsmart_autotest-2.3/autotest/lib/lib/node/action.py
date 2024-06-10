"""
    Do the action for a node
"""
import time
from dataclasses import dataclass, field
from ramda import path_or
from selenium.common.exceptions import (
    StaleElementReferenceException,
    NoSuchElementException,
    ElementClickInterceptedException,
)
from autotest.lib.lib.node.node import Nodes

GLOBAL_WAIT_TIME = 4


@dataclass
class Action:
    """
    This class will perform the action
    """

    driver: type
    nodes: Nodes
    results: list = field(default_factory=list)

    def find_by_xpath(self, xpath: str, many : bool = False):
        """
        Return element
        """
        if many:
            return self.driver.find_elements_by_xpath(xpath)
        return self.driver.find_element_by_xpath(xpath)

    def click(self, element, node_action):
        """
        This function will click the element
        """
        print("==========clicking the element", element, node_action)
        clicked = element.click()
        print("----------clicked ->", clicked)
        return clicked

    def input_text(self, element, node_action):
        """
        This function will input the text into element
        """
        return element.send_keys(node_action.data["input_text"])
    
    def input_text_list(self, element : list, node_action : list):
        """
            send keys to list
        """
        for idx, input_box in enumerate(element):
            input_box.send_keys(path_or("",[idx], node_action.data["input_text_list"]))
    
    def switch_to_iframe(self, element):
        """
            switch to iframe
        """
        iframe_index = 0  # Index of the iframe you want to switch to
        self.driver.switch_to.frame(iframe_index)
    
    def switch_to_default(self, element):
        """
            switch to default
        """
        self.driver.switch_to.default_content()

    def element_text(self, node_action=None, ele_identifier=""):
        """
        This function will find the element by text
        """
        # xpath="//button[contains(text(), '" + element_text + "')]"
        element_text = ele_identifier or node_action.data["element_text"]
        try:
            element = self.find_by_xpath(
                xpath="//button[contains(text(), '" + element_text + "')]"
            )
        except NoSuchElementException as err:
            print("err", err)
            element = self.find_by_xpath(
                xpath="//*[contains(text(), '" + element_text + "')]"
            )
        return element

    def element_type(self, node_action=None, ele_identifier=""):
        """
        This function will find the element by text
        """
        element_type = ele_identifier or node_action.data["element_type"]
        element = self.find_by_xpath(xpath="//input[@type='" + element_type + "']")
        return element
    
    def element_value(self, node_action=None, ele_identifier=""):
        """
        This function will find the element by value
        """
        element_value = ele_identifier or node_action.data["element_value"]
        element = self.find_by_xpath(xpath="//input[@value='" + element_value + "']")
        return element

    def element_placeholder(self, node_action=None, ele_identifier=""):
        """
        This function will find the element by its place holder
        """
        element_placeholder = ele_identifier or node_action.data["element_placeholder"]
        element = self.driver.find_element_by_css_selector(
            'input[placeholder="' + element_placeholder + '"]'
        )

        return element

    def element_id(self, node_action=None, ele_identifier=""):
        """
        finds element by id
        """
        element_id = ele_identifier or node_action.data["element_id"]
        try:
            print("===========Element id==>", element_id)
            element = self.driver.find_element_by_id(element_id)
        except StaleElementReferenceException:
            time.sleep(3)
            element = self.driver.find_element_by_id(element_id)
        return element

    def data_test_id(self, node_action=None, ele_identifier=""):
        """
        Locate the element by test id
        """
        data_test_id = ele_identifier or node_action.data["data_test_id"]
        try:
            print("===========data_test_id==>", data_test_id)
            element = self.driver.find_element_by_css_selector(
                '[data-test-id="' + data_test_id + '"]'
            )
        except StaleElementReferenceException:
            time.sleep(3)
            element = self.driver.find_element_by_css_selector(
                '[data-test-id="' + data_test_id + '"]'
            )
        return element
    
    def find_element_by_input_mode(self, node_action : None):
        """
            This function will find elements by class name
        """
        xpath_expression = f'//input[@inputmode="{node_action.data["find_element_by_input_mode"]}"]'

        # Find elements that match the XPath expression
        input_boxes = self.find_by_xpath(xpath=xpath_expression, many=True)
        return input_boxes

    def do_nothing(self,element, node_action):
        """
            do nothing
        """
        time.sleep(GLOBAL_WAIT_TIME)

    def do_action(self, node_action):
        """
        This will do the action
        """
        element_func = getattr(self, node_action.find_by)
        element = element_func(node_action)
        print("Element found==>", element)
        action_func = getattr(self, node_action.action_type)
        action_func(element=element, node_action=node_action)
        wait_time = path_or("", ["wait_time"], node_action.data)
        if wait_time:
            print("Waiting -->", wait_time)
            time.sleep(wait_time)
        return ""

    def do_validations(self, validations: list):
        """
        This function will do the validations
        """
        for validation in validations:
            find_by = path_or("", ["find_by"], validation)
            element_func = getattr(self, find_by)
            element_func(ele_identifier=validation["data"][find_by])
        return ""

    def start(self):
        """
        This function will start the node actions
        """
        for idx, node in enumerate(self.nodes.nodes):
            intent_data = node.intent_data
            print("-------node", node)
            node_results = []
            errors = []
            for node_action in node.actions:
                try:
                    time.sleep(GLOBAL_WAIT_TIME)
                    self.do_validations(
                        validations=path_or([], ["pre"], node_action.validations)
                    )
                    action = self.do_action(node_action=node_action)
                    print("completed=======>>>>>>>>>>>", action)
                    node_results.append(True)
                except (
                    NoSuchElementException,
                    ElementClickInterceptedException,Exception
                ) as err:
                    ignore_error = path_or("",["ignore_error"], node_action.data)
                    if ignore_error:
                        continue
                    print("err--->", err)
                    node_results.append(False)
                    errors.append(err)

            res = {
                "question": path_or("", ["question"], intent_data)
                or path_or("", ["question_id"], intent_data),
                "status": "PASS" if False not in node_results else "FAIL",
                "errors" : str(errors) if False in node_results else ""
            }
            self.results.append(res)

        return self.results
