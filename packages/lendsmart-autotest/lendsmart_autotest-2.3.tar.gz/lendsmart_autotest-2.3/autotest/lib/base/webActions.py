from cmath import log
import inspect
import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC



class webActions:
    def __init__(self, driver, wait, log):
        self.driver = driver
        self.wait = wait
        self.log = log



    def findElement(self, xpath):
        try:
            element=self.driver.find_element_by_xpath(xpath)
            self.log.log.debug("found element : " + xpath)
            return element

        except Exception as e:
            exeMsg=type(e).__name__ + " : " + str(e)
            self.log.log.error("Exception occured in => "+ self.getCallerFunctions())
            self.log.log.error("Unable to find element : " + xpath)
            self.log.log.error(exeMsg)
            raise e



    def findElements(self, xpath):
        try:
            elements=self.driver.find_elements_by_xpath(xpath)
            self.log.log.debug("found elements : " + xpath)
            return elements

        except Exception as e:
            exeMsg=type(e).__name__ + " : " + str(e)
            self.log.log.error("Exception occured in => "+ self.getCallerFunctions())
            self.log.log.error("Unable to find elements : " + xpath)
            self.log.log.error(exeMsg)
            raise e



    def waitAndFindElement(self, xpath, ret=False):
        try:
            element = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
            self.log.log.debug("found element : " + xpath)
            return element

        except Exception as e:
            exeMsg=type(e).__name__ + " : " + str(e)
            self.log.log.error("Exception occured in => "+ self.getCallerFunctions())
            self.log.log.error("Unable to find element : " + xpath)
            self.log.log.error(exeMsg)
            if(ret):
                return False
            else:
                raise e



    def waitAndFindElements(self, xpath):
        try:
            elements = self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, xpath)))
            self.log.log.debug("found elements : " + xpath)
            return elements

        except Exception as e:
            exeMsg=type(e).__name__ + " : " + str(e)
            self.log.log.error("Exception occured in => "+ self.getCallerFunctions())
            self.log.log.error("Unable to find elements : " + xpath)
            self.log.log.error(exeMsg)
            raise e



    def sendKeysOnElement(self, xpath, text):
        try:
            self.driver.find_element_by_xpath(xpath).send_keys(text)
            if (text not in [Keys.BACKSPACE, Keys.DOWN, Keys.UP, Keys.RETURN, Keys.ENTER]):
                self.log.log.debug("entered " + str(text) + " on element : " + xpath)

        except Exception as e:
            exeMsg=type(e).__name__ + " : " + str(e)
            self.log.log.error("Exception occured in => "+ self.getCallerFunctions())
            self.log.log.error("Unable to enter text in element : " + xpath)
            self.log.log.error(exeMsg)
            raise e



#newcode
    def sendKeys(self, element, text):
        try:
            self.log.log.info("inside sendkey")
            element.send_keys(text)


        except Exception as e:
            exeMsg=type(e).__name__ + " : " + str(e)
            self.log.log.error("Exception occured in => "+ self.getCallerFunctions())

            self.log.log.error(exeMsg)
            raise e
#newcode



    def clickOnElement(self, xpath):
        try:
            self.log.log.info("Inside Click on Element")
            self.driver.find_element_by_xpath(xpath).click()
            self.log.log.debug("clicked on element : " + xpath)

        except Exception as e:
            exeMsg=type(e).__name__ + " : " + str(e)
            self.log.log.error("Exception occured in => "+ self.getCallerFunctions())
            self.log.log.error("Unable to click on element : " + xpath)
            self.log.log.error(exeMsg)
            raise e



    def waitAndSendKeysOnElement(self, xpath, text, ret=False):
        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath))).send_keys(text)
            self.log.log.debug("entered " + text + " on element : " + xpath)

        except Exception as e:
            exeMsg=type(e).__name__ + " : " + str(e)
            self.log.log.error("Exception occured in => "+ self.getCallerFunctions())
            self.log.log.error("Unable to enter text in element : " + xpath)
            self.log.log.error(exeMsg)
            raise e



    def waitAndClickOnElement(self, xpath):
        try:
            self.log.log.info("Inside Wait and clickonElement")
            self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath))).click()
            self.log.log.debug("clicked on element : " + xpath)
            self.log.log.info("Element Clicked")

        except Exception as e:
            exeMsg=type(e).__name__ + " : " + str(e)
            self.log.log.error("Exception occured in => "+ self.getCallerFunctions())
            self.log.log.error("Unable to click on element : " + xpath)
            self.log.log.error(exeMsg)
            raise e

    def clearContent(self, xpath):
            self.log.log.info("Inside clear content for input box")
            element=self.driver.find_element_by_xpath(xpath)
            element.clear()




    def isElementVisible(self, xpath):
        try:
            elements=self.driver.find_elements_by_xpath(xpath)
            self.log.log.debug(elements)
            if (len(elements) == 1):
                self.log.log.debug("Element visible : " + xpath)
                return True
            else:
                self.log.log.debug("Element not visible : " + xpath)
                return False

        except Exception as e:
            exeMsg=type(e).__name__ + " : " + str(e)
            self.log.log.error("Exception occured in => "+ self.getCallerFunctions())
            self.log.log.error(exeMsg)
            raise e



    def waitForInvisibilityOfElement(self, xpath):
        try:
            if (self.wait.until(EC.invisibility_of_element_located((By.XPATH, xpath)))):
                self.log.log.debug("Element invisible : " + xpath)
                return True
            else:
                self.log.log.debug("Element not invisible : " + xpath)
                return False

        except Exception as e:
            exeMsg=type(e).__name__ + " : " + str(e)
            self.log.log.error("Exception occured in => "+ self.getCallerFunctions())
            self.log.log.error(exeMsg)
            raise e



    def waitForPresenceOfElements(self, xpath):
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
            self.log.log.debug("element present : " + xpath)
            return elements

        except Exception as e:
            exeMsg=type(e).__name__ + " : " + str(e)
            self.log.log.error("Exception occured in => "+ self.getCallerFunctions())
            self.log.log.error("element not present : " + xpath)
            self.log.log.error(exeMsg)
            raise e


#Explicit Wait
    def waitForElementToBeClickable(self, xpath):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
        try:
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            self.log.log.debug("element clickable : " + xpath)
            return element

        except Exception as e:
            exeMsg=type(e).__name__ + " : " + str(e)
            self.log.log.error("Exception occured in => "+ self.getCallerFunctions())
            self.log.log.error("element not clickable : " + xpath)
            self.log.log.error(exeMsg)
            raise e



    def getCallerFunctions(self):
        function_name = ""
        curr_frame = inspect.currentframe().f_back
        stmt = []
        while (function_name != "pytest_pyfunc_call"):
            (filename, line_number, function_name, lines, index) = inspect.getframeinfo(curr_frame)
            stmt.append("%s:%s:%s:" % (filename.split("\\")[-1], line_number, function_name))

            previous_frame = curr_frame.f_back
            (filename, line_number, function_name, lines, index) = inspect.getframeinfo(previous_frame)
            curr_frame = previous_frame

        stmt = str(stmt[::-1])
        stmt = re.sub("[\',\[\]]", '', stmt)
        return stmt

    def scrollToView(self, xpath):
        try:
            self.log.log.info("Inside Click on Element")
            element = self.driver.find_element_by_xpath(xpath)
            self.driver.execute_script("arguments[0].scrollIntoView;", element)
            self.log.log.debug("clicked on element : " + xpath)

        except Exception as e:
            exeMsg=type(e).__name__ + " : " + str(e)
            self.log.log.error("Exception occured in => "+ self.getCallerFunctions())
            self.log.log.error("Unable to click on element : " + xpath)
            self.log.log.error(exeMsg)
            raise e

    def assertElementTextEqualsValue(self, xpath, value):
        element = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        # element.click()
        assert element.get_attribute("innerText") == value

    def assertInputTextEqualsValue(self, xpath, value):
        element = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        element.click()
        assert element.get_attribute("value") == value

    def assertInputContainsValue(self, xpath, value):
        element = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        input_value = element.get_attribute("value")
        self.log.log.info("ASSERT: " +value+ " Contains in : " + input_value)
        assert value in input_value


    def assertElementContainsText(self, xpath, value):
        element = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        elementInnerText = element.get_attribute("innerText")
        self.log.log.info("ASSERT: " +value+ " Contains in : " + elementInnerText)
        assert value in elementInnerText

    def assertElementIsChecked(self, xpath):
        element = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        checkedBoolean = element.get_attribute("checked")
        self.log.log.info("ASSERT: " +xpath+ " is " +checkedBoolean+ "")
        assert True == checkedBoolean

    def assertElementExists(self, xpath):
        element = self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, xpath)))
        assert len(element) > 0

    def assertInputTextEqualsValue(self, xpath, value):
        element = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        element.click()
        assert element.get_attribute("value") == value

    def assertInputContainsValue(self, xpath, value):
        element = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        input_value = element.get_attribute("value")
        self.log.log.info("ASSERT: " + value + " Contains in : " + input_value)
        assert value in input_value

    def assertElementContainsText(self, xpath, value):
        element = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        elementInnerText = element.get_attribute("innerText")
        self.log.log.info("ASSERT: " + value + " Contains in : " + elementInnerText)
        assert value in elementInnerText

    def assertElementIsChecked(self, xpath):
        element = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        checkedBoolean = element.get_attribute("checked")
        self.log.log.info("ASSERT: " + xpath + " is " + checkedBoolean + "")
        assert True == checkedBoolean
