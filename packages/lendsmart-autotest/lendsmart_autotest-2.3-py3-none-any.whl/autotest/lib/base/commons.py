import base64
import json
import random
import string
import time

import keyboard
# import pyautogui
import requests
from base.webActions import webActions
from selenium.webdriver.support.select import Select

from conftest import env
#from configurations.BC.constants import xpathSkipAndProceedButton, xpathMyComputerButton, xpathBrowseOption,xpathSelectedFilename, xpathSubmitButton
from pages.MCA.uploadPage import uploadPage
from configurations.common_config import environment
from configurations.MCA.constants import xpathTypeMessageInput, xpathSendMessageButton, xpathOpenDatePicker, xpathSelectYear, xpathSelectMonth
from configurations.MCA.test_data_Test_001_mca_no_documents import businessIndustry, businessPhoneNo, fico, averageMonthlySales, fundingRequired



class commons(webActions):
    def __init__(self, driver, wait, log):
        super().__init__(driver, wait, log)
        self.obj_uploadPage = uploadPage(driver, wait, log)
        self.driver = driver
        self.wait = wait
        self.log = log



    def isQuestionDisplayed(self, xpath, ret=False):
        time.sleep(2)
        if(self.waitAndFindElement(xpath, ret)):
            return True
        else:
            return False



    def isWarningDisplayed(self, xpath):
        time.sleep(2)
        if(self.waitAndFindElement(xpath, ret=True)):
            return True
        else:
            return False



    def isAnswerDisplayed(self, xpath):
        time.sleep(2)
        if(self.isElementVisible(xpath)):
            return True
        else:
            return False



    def enterAnswer(self, question, answer, inputBox=xpathTypeMessageInput, sendButton=xpathSendMessageButton):
        if(self.waitAndFindElement(question)):
            self.log.log.info("Question displayed")
            self.log.log.info("Entering text : " + answer)
            self.sendKeysOnElement(inputBox, answer)
            self.log.log.info("Clicking on Send")
            self.clickOnElement(sendButton)



    def selectDate(self, question, date, day):
        date = date.split("/")
        if(self.waitAndFindElement(question)):
            self.log.log.info("Question displayed")
            self.log.log.info("Clicking on Date Picker")
            self.clickOnElement(xpathOpenDatePicker)
            year = Select(self.findElement(xpathSelectYear))
            month = Select(self.findElement(xpathSelectMonth))
            self.log.log.info("Selecting Year : " + date[2])
            year.select_by_value(date[2])
            self.log.log.info("Selecting Month : " + date[0])
            month.select_by_value(str(int(date[0]) - 1))
            self.log.log.info("Selecting Day : " + date[1])
            self.waitAndClickOnElement(day)
            self.log.log.info("Clicking on Send")
            self.clickOnElement(xpathSendMessageButton)



    def selectOption(self, question, answer, optionList, docDetailsList=None):
        if (self.waitAndFindElement(question)):
            self.log.log.info("Question displayed")

            if(answer=="yes"):
                self.log.log.info("Selecting Yes")
                self.clickOnElement(optionList[0])
            elif(answer=="no"):
                self.log.log.info("Selecting No")
                self.clickOnElement(optionList[1])

            elif(answer=="own"):
                self.log.log.info("Selecting Own")
                self.clickOnElement(optionList[0])
            elif(answer=="rent"):
                self.log.log.info("Selecting Rent")
                self.clickOnElement(optionList[1])

            elif(answer=="later"):
                self.log.log.info("Selecting I don't have access")
                self.clickOnElement(optionList[0])
            elif(answer=="cloud"):
                self.log.log.info("Selecting Cloud Storage")
                self.clickOnElement(optionList[1])
                self.obj_uploadPage.uploadFromCloud(docDetailsList)
            elif(answer=="computer"):
                self.log.log.info("Selecting My Computer")
                self.clickOnElement(optionList[2])
                self.obj_uploadPage.uploadFromComputer(docDetailsList)
            elif(answer=="mobile"):
                self.log.log.info("Selecting Send pictures from Mobile")
                self.clickOnElement(optionList[3])
                self.obj_uploadPage.uploadFromMobile(docDetailsList)
            elif(answer=="letusdoit"):
                self.log.log.info("Selecting Connect your bank")
                self.clickOnElement(optionList[4])
                self.obj_uploadPage.uploadFromLiveBank(docDetailsList)

            elif (answer=="Sole proprietor"):
                self.log.log.info("Selecting Sole proprietor")
                self.clickOnElement(optionList[0])
            elif (answer=="Corp"):
                self.log.log.info("Selecting Corp")
                self.clickOnElement(optionList[1])
            elif (answer=="LLC"):
                self.log.log.info("Selecting LLC")
                self.clickOnElement(optionList[2])
            elif (answer=="Partnership"):
                self.log.log.info("Selecting Partnership")
                self.clickOnElement(optionList[3])
            elif (answer=="LLP"):
                self.log.log.info("Selecting LLP")
                self.clickOnElement(optionList[4])
            elif (answer=="Other"):
                self.log.log.info("Selecting Other")
                self.clickOnElement(optionList[5])



    def verifyAnswerDisplayed(self, xpath1, xpath2=None, answer=None):
        if(answer==None):
            if (self.waitAndFindElement(xpath1)):
                self.log.log.info("Answer Displayed")

        elif(answer=="later"):
            if (self.waitAndFindElement(xpath2)):
                self.log.log.info("Answer Displayed")

        elif(answer in ["cloud", "letusdoit", "computer", "mobile"]):
            if (self.waitAndFindElement(xpath1)):
                self.log.log.info("Answer Displayed")

        elif(answer=="own"):
            if (self.waitAndFindElement(xpath1)):
                self.log.log.info("Answer Displayed")

        elif(answer=="rent"):
            if (self.waitAndFindElement(xpath2)):
                self.log.log.info("Answer Displayed")

        elif(answer=="yes"):
            if (self.waitAndFindElement(xpath1)):
                self.log.log.info("Answer Displayed")

        elif(answer=="no"):
            if (self.waitAndFindElement(xpath2)):
                self.log.log.info("Answer Displayed")



    def compareAnswers(self, userAnswers, systemAnswers, heading, byValue=False):
        for i in range(0, len(systemAnswers)):

            if(type(heading[i]) != type("string")):
                heading[i]=heading[i].text

            if(type(systemAnswers[i]) != type("string")):
                if (byValue):
                    systemAnswers[i] = systemAnswers[i].get_attribute("value")
                else:
                    systemAnswers[i] = systemAnswers[i].text


        for i in range(0, len(userAnswers)):
            if (userAnswers[i] != systemAnswers[i]):
                self.log.log.info("INCORRECT ANSWER: "+ heading[i] +" :user answer = " + userAnswers[i] + " && system answer = " + systemAnswers[i])
            else:
                self.log.log.info("CORRECT ANSWER: "+ heading[i] +" :user answer = " + userAnswers[i] + " && system answer = " + systemAnswers[i])



    def uploadFromMyComputer(self, file, filename):
        if (file == "SkipAndProceed"):
            self.log.log.info("Skipping Upload")
            self.log.log.info("Clicking on SkipAndProceed button")
            self.clickOnElement(xpathSkipAndProceedButton)
        elif (file == "MyComputer"):
            self.log.log.info("Uploading from My Computer")
            self.log.log.info("Clicking on MyComputer button")
            self.clickOnElement(xpathMyComputerButton)
            self.log.log.info("Clicking on browse button")
            self.waitAndClickOnElement(xpathBrowseOption)

            time.sleep(2)
            self.log.log.info("Selecting File to be uploaded")

            keyboard.write(filename, delay=0.10)
            # pyautogui.write(filename, interval=0.25)
            time.sleep(2)
            keyboard.send('enter')
            # pyautogui.press('enter')
            self.log.log.info("Selected File to be uploaded")
            self.waitAndFindElement(xpathSelectedFilename)
            self.log.log.info("Clicking on Submit button")
            self.waitAndClickOnElement(xpathSubmitButton)



    def uploadDocument(self, email, password, docName, docPath, docCategory, docArtifact):

        with open(docPath, "rb") as file:
            encoded = base64.b64encode(file.read())
            content = encoded.decode()

        acc_id, loanapp_id, loanrole_id = self.loginAPI(email, password)
        self.uploadDocsAPI(acc_id, loanapp_id, loanrole_id, docName, content, docCategory, docArtifact)



    def loginAPI(self, email, password):
        url = environment[env]["loginURI"]

        payload = json.dumps({
            "email": email,
            "password": password
        })

        headers = {'Content-Type': 'application/json'}

        response = requests.request("POST", url, headers=headers, data=payload)

        if (response.status_code == 200):
            resp = response.json()
            acc_id = resp['id']
            loanapp_id = resp['context'][0]['loanapp_id']
            loanrole_id = resp['context'][0]['loanrole_id'][0]
            return acc_id, loanapp_id, loanrole_id
        else:
            self.log.log.error("Error while calling login API")



    def uploadDocsAPI(self, acc_id, loanapp_id, loanrole_id, docName, content, docCategory, docArtifact):
        url = environment[env]["uploadDocsURI"]

        payload = json.dumps({
            "content": content,
            "object_meta": {
                "name": "test_" + docName,
                "account": acc_id,
                "owner_references": [
                    {
                        "kind": "LoanAppRole",
                        "api_version": "v1",
                        "uid": loanrole_id,
                        "name": loanrole_id,
                        "block_owner_deletion": False
                    },
                    {
                        "kind": "LoanApp",
                        "api_version": "v1",
                        "uid": loanapp_id,
                        "name": loanapp_id,
                        "block_owner_deletion": False
                    }
                ],
                "labels": {
                    "lendsmart_sh/sbappp": "yes",
                    "category": docCategory
                }
            },
            "remote_bucket": "apptest.fundaloan.loandocs",
            "remote_filename": "test_" + docName,
            "remote_folder": acc_id,
            "metadata": {
                "artifact": docArtifact
            }
        })

        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.request("POST", url, headers=headers, data=payload)

            if (response.status_code == 200):
                self.log.log.info("Uploaded " + docName + " successfully")
            else:
                self.log.log.error("Unable to upload " + docName)

        except Exception as e:
            exeMsg = type(e).__name__ + " : " + str(e)
            print(e)
            print(exeMsg)






def createAccount(emailid):
    url = loginURI

    payload = json.dumps({
        "email": emailid,
        "first_name": emailid[0:8],
        "last_name": emailid[9:17],
        "password": "Speed@123",
        "status": "active",
        "metadata": {
            "lendsmart_sh/naic_industry": businessIndustry,
            # "lendsmart_sh/prequalification_business_phone_number": businessPhoneNo,
            "lendsmart_sh/prequalification_fico": fico,
            "lendsmart_sh/prequalification_monthly_revenue": averageMonthlySales,
            "lendsmart_sh/prequalification_requested_amount": fundingRequired,
            "role": "home_buyer"
        }
    })

    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if(response.status_code==200):
        return True
    else:
        return False



def generateEmailID():
    size = 8
    chars = string.ascii_uppercase + string.digits
    emailID = 'testauto_' + ''.join(random.choice(chars) for _ in range(size)).lower() + "@mailnesia.com"
    return emailID



def changeImports(file, mod, str):
    f = open(file, "r")
    list_of_lines = f.readlines()
    line = list_of_lines[3]

    text = (line[line.index(str) + 18:line.index(' import')])
    linenew = line.replace(text, mod)
    list_of_lines[3] = linenew

    f = open(file, "w")
    f.writelines(list_of_lines)
    f.close()



def changeTestData(testDataFile, attribute, value):
    with open(testDataFile, 'r+') as g:
        text = g.read()
        text = text.replace(attribute, value)
        g.seek(0)
        g.write(text)
        g.truncate()