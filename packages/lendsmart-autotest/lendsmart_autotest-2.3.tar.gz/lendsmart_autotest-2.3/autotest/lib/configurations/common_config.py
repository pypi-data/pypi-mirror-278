chromiumUserAgent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36"
chromeUserAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"

chromeDriverPathLinux="/home/becca/Downloads/chromedriver_linux64/chromedriver"
chromeDriverPathWin="D:\\Installers\\Browsers\\chromedriver_win32\\chromedriver.exe"
geckoDriverPathWin= "D:\\Installers\\Browsers\\geckodriver-v0.27.0-win64\\geckodriver.exe"
edgeDriverPathWin= "D:\\Installers\\Browsers\\edgedriver_win64\\msedgedriver.exe"



testRailEndpoint = "https://lendsmartlabs.testrail.io/"
testRailUser = "accounts@lendsmart.ai"
testRailPassword = "mEVZlQQMO8.EbJcL72gQ"

base_testrail_plan_url = "https://lendsmartlabs.testrail.io/index.php?/plans/view/"
base_testrail_run_url = "https://lendsmartlabs.testrail.io/index.php?/runs/view/"

slack_testrail_app_url = "https://hooks.slack.com/services/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"


BC = "BC"
CSB = "CSB"
ROMP = "ROMP"
STAT = "STAT"
A4CB = "A4CB"
MIDWEST="MIDWEST"
LEGENCE="LEGENCE"

waitTime=60
sleepTime=2


environment = {
    "BC_qa" :
        {
            "baseURL" : "https://breakoutfinanceuat.lendsmart.ai",
            "loginURI" : "https://testapi.lendsmart.ai/api/v1/apptest/login",
            "uploadDocsURI" : "https://testapi.lendsmart.ai/api/v1/apptest/document_pointers/upload",
            "testRailProjectID":"1",
            "testRailSuiteID":"1"
        },

    "BC_dev":
        {
            "baseURL": "https://breakoutfinancedev.lendsmart.ai/login",
            "loginURI": "https://matapi.lendsmart.ai/api/v1/breakoutcapital/login",
            "uploadDocsURI": "https://matapi.lendsmart.ai/api/v1/breakoutcapital/document_pointers/upload",
            "testRailProjectID": "1",
            "testRailSuiteID": "1"
        },

    "BC_prod":
        {
            "baseURL": "prod baseURL",
            "loginURI": "prod loginURI",
            "uploadDocsURI": "prod uploadDocsURI",
            "testRailProjectID": "1",
            "testRailSuiteID": "1"
        },

    "SUTTONBANK_qa" :
        {
            "baseURL" : "https://suttonbankdev.lendsmart.ai/",
            "loginURI" : "https://devapi.lendsmart.ai/api/v1/suttonbankdev/login",
            "uploadDocsURI" : "https://devapi.lendsmart.ai/api/v1/suttonbankdev/document_pointers/upload"
        },

    "ROMP_qa" :
        {
            "baseURL" : "https://roundpointmortgagedev.lendsmart.ai/login",
            "loginURI" : "https://testapi.lendsmart.ai/api/v1/roundpointmortgagedev/login",
            "uploadDocsURI" : "https://testapi.lendsmart.ai/api/v1/roundpointmortgagedev/document_pointers/upload"
        },

    "ROMP_prod" :
        {
            "baseURL" : "https://roundpointmortgage.lendsmart.ai/login",
            "loginURI" : "https://testapi.lendsmart.ai/api/v1/roundpointmortgage/login",
            "uploadDocsURI" : "https://testapi.lendsmart.ai/api/v1/roundpointmortgage/document_pointers/upload"
        },

    "CSB_qa" :
        {
            "baseURL" : "https://csbnetdev.lendsmart.ai/login",
            "loginURI" : "https://testapi.lendsmart.ai/api/v1/csbnetdev/login",
            "uploadDocsURI" : "https://testapi.lendsmart.ai/api/v1/csbnetdev/document_pointers/upload",
            "testRailProjectID": "16",
            "testRailSuiteID": "149"

        },

    "CSB_prod" :
        {
            "baseURL" : "https://csbnet.lendsmart.ai/login",
            "loginURI" : "https://testapi.lendsmart.ai/api/v1/csbnet/login",
            "uploadDocsURI" : "https://testapi.lendsmart.ai/api/v1/csbnet/document_pointers/upload",
            "testRailProjectID": "16",
            "testRailSuiteID": "149"
        },

    "STAT_qa" :
        {
            "baseURL" : "https://strattonequitiesdev.lendsmart.ai/login",
            "loginURI" : "https://testapi.lendsmart.ai/api/v1/strattonequitiesdev/login",
            "uploadDocsURI" : "https://testapi.lendsmart.ai/api/v1/strattonequitiesdev/document_pointers/upload",
            "testRailProjectID" : "12",
            "testRailSuiteID":"134"
        },

    "STAT_prod" :
        {
            "baseURL" : "https://strattonequities.lendsmart.ai/login",
            "loginURI" : "https://testapi.lendsmart.ai/api/v1/strattonequities/login",
            "uploadDocsURI" : "https://testapi.lendsmart.ai/api/v1/strattonequities/document_pointers/upload",
            "testRailProjectID" : "12",
            "testRailSuiteID":"134"
        },


    "A4CB_qa":
        {
            "baseURL" : "https://a4cbdev.lendsmart.ai/login",
            "loginURI" : "https://testapi.lendsmart.ai/api/v1/a4cbdev/login",
            "uploadDocsURI" : "https://testapi.lendsmart.ai/api/v1/a4cbdev/document_pointers/upload",
            "testRailProjectID": "13",
            "testRailSuiteID": "135"
        },

    "A4CB_prod":
        {
            "baseURL" : "https://a4cb.lendsmart.ai/login",
            "loginURI" : "https://testapi.lendsmart.ai/api/v1/a4cb/login",
            "uploadDocsURI" : "https://testapi.lendsmart.ai/api/v1/a4cb/document_pointers/upload",
            "testRailProjectID": "13",
            "testRailSuiteID": "135"
        },

    "MIDWEST_qa":
        {
            "baseURL" : "https://mbwidev.lendsmart.ai//login",
            "loginURI" : "https://testapi.lendsmart.ai/api/v1/mbwidev/login",
            "uploadDocsURI" : "https://testapi.lendsmart.ai/api/v1/mbwidev/document_pointers/upload",
            "testRailProjectID" : "17",
            "testRailSuiteID" : "172"
        },


    "MIDWEST_prod":
        {
            "baseURL" : "https://mbwi.lendsmart.ai/login",
            "loginURI" : "https://testapi.lendsmart.ai/api/v1/mbwi/login",
            "uploadDocsURI" : "https://testapi.lendsmart.ai/api/v1/mbwi/document_pointers/upload",
            "testRailProjectID" : "17",
            "testRailSuiteID":"172"
       },

    "LEGENCE_qa":
        {
            "baseURL": "https://legencebankdev.lendsmart.ai/login",
            "loginURI": "https://testapi.lendsmart.ai/api/v1/legencebankdev/login",
            "uploadDocsURI": "https://testapi.lendsmart.ai/api/v1/legencebankdev/document_pointers/upload",
            "testRailProjectID": "15",

            "testRailSuiteID": "174"
        },

    "LEGENCE_prod":
        {
            "baseURL": "https://legencebank.lendsmart.ai/login",
            "loginURI": "https://testapi.lendsmartbank.ai/api/v1/legence/login",
            "uploadDocsURI": "https://testapi.lendsmart.ai/api/v1/legencebank/document_pointers/upload",
            "testRailProjectID": "15",

            "testRailSuiteID": "174"
        }

}