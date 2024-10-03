from selenium import webdriver
from jenkinsfunctions import fillform, checksuccess, differenceinminutes,test
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service

import time
import datetime
import yaml

yaml_file = open("config/jenkins-deployment-config.yml", 'r')
config = yaml.load(yaml_file, yaml.FullLoader)

jenkins = 'jenkins-global'
environment = config[jenkins]['environment']
globalActionEnabled = bool(config[jenkins]['globalActionEnabled'])
globalAction = config[jenkins]['globalAction']
baseurl = config[jenkins]['baseurl']
J_USERNAME = config[jenkins]['J_USERNAME']
J_PASS = config[jenkins]['J_PASS']
deployment = config['deployment']
successMsg = config[jenkins]['successMsg']
maxTimeForTab = config[jenkins]['maxTimeForTab']
maxTimeForWholeRun = config[jenkins]['maxTimeForWholeRun']
sleepBeforeEachCycleStart = config[jenkins]['sleepBeforeEachCycleStart']
sleepBeforeEachTabOpens = config[jenkins]['sleepBeforeEachTabOpens']

# LOGIN
options = Options()
# options.add_experimental_option("detach", True)
options.binary_location = "/chrome-web-driver/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
service = Service(executable_path='/chrome-web-driver/chromedriver')

driver = webdriver.Chrome(service = service, options=options)
driver.get(baseurl + "/login?from=%2F")
driver.find_element(By.ID, 'j_username').send_keys(J_USERNAME)
driver.find_element(By.NAME, 'j_password').send_keys(J_PASS)
driver.find_element(By.NAME, 'Submit').click();
time.sleep(2)

# find start time after login
startTime = datetime.datetime.now()
print("startTime for deployment >> ", startTime)


# FILL UP FORM
tabindex = 0
deployedconsolelinks = fillform(driver, deployment, baseurl, tabindex, environment, globalActionEnabled, globalAction, sleepBeforeEachTabOpens)
#deployedconsolelinks = test(driver, deployment, baseurl, tabindex, environment, globalActionEnabled, globalAction, sleepBeforeEachTabOpens)
print("deployedconsolelinks >> ", deployedconsolelinks)
wait = WebDriverWait(driver, maxTimeForTab)



# MONITOR COONSOLE
checkconsole = True
while checkconsole:
    currentTime = datetime.datetime.now()
    print("current time >> ", datetime.datetime.now())
    allTabs = driver.window_handles
    print("size of all tabs inside ", len(allTabs))
    if len(allTabs) == 1:
        checkconsole = False
        print(" WINDOW HAS 1 TAB OPEN !")
        print(" ALL TASKS COMPLETED !")
    elif differenceinminutes(startTime, currentTime) > maxTimeForWholeRun:
        checkconsole = False
        print("SCRIPT HAS FAILURES, olunga check panu da DABUR !")
        print("current active tabs ")
        for tab in allTabs:
            print(tab)
    elif len(allTabs) > 1:
        for tab in allTabs:
            driver.switch_to.window(tab)
            if "/console" in driver.current_url:
                checksuccess(wait, driver, successMsg)
        time.sleep(sleepBeforeEachCycleStart)

print("script took = ", differenceinminutes(startTime, datetime.datetime.now()), " minutes to get completed")
time.sleep(10)
driver.quit()
