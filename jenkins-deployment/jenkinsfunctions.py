from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
import time


# FILL UP FORM
def fillform(driver, deployment, baseurl, tabindex, environment, globalActionEnabled, globalAction, sleepBeforeEachTabOpens):
    deployedconsolelinks = []
    for service, value in deployment.items():
        deploy = bool(value.get('deploy'))
        print("service = " + service + " deploy = " + str(deploy) )
        if globalActionEnabled:
            action = globalAction
        else:
            action = str(value.get('action'))
        if deploy:
            tabindex = tabindex + 1
            txt = str(value.get('url')).replace("ENVIRONMENT", environment)
            url = baseurl + txt
            version = str(value.get('version'))


            print("tab index " + str(tabindex) + " action " + action + " version " + str(version)
                  + " url " + url + " deploy " + str(deploy))

            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[tabindex])
            driver.get(url)
            select = Select(
                driver.find_element(By.XPATH, '//*[@id="main-panel"]/form/table/tbody[1]/tr[1]/td[3]/div/select'))
            select.select_by_visible_text(action)
            select = Select(
                driver.find_element(By.XPATH, '//*[@id="main-panel"]/form/table/tbody[2]/tr[1]/td[3]/div/select'))
            select.select_by_visible_text(service)

            ## docker version
            ##inputVersion = driver.find_element(By.XPATH,'//*[@id="main-panel"]/form/table/tbody[6]/tr[1]/td[3]/div/input[2]')

            ## eks version
            inputVersion = driver.find_element(By.XPATH,
                                               '//*[@id="main-panel"]/form/table/tbody[3]/tr[1]/td[3]/div/input[2]')
            inputVersion.clear()
            inputVersion.send_keys(version)
            driver.find_element(By.XPATH, '//*[@id="yui-gen1-button"]').click()
            deployedHrefElement = driver.find_element(By.XPATH,
                                                      '//*[@id="buildHistory"]/div[2]/table/tbody/tr[2]/td/div[1]/a')
            deployedherf = deployedHrefElement.get_attribute('href')
            print("href >> " + deployedherf)
            #deployedconsolelinks.append(baseurl + deployedHrefElement.get_attribute('href') + 'console')
            #driver.get(baseurl + deployedHrefElement.get_attribute('href') + 'console')

            deployedconsolelinks.append(deployedherf + 'console')
            driver.get(deployedherf + 'console')

            time.sleep(sleepBeforeEachTabOpens)
    return deployedconsolelinks


# CHECK SUCCESS MSG IS PRESENT IN JENKINS CONSOLE
def checksuccess(wait, driver, successMsg):
    try:
        wait.until(ec.text_to_be_present_in_element((By.CLASS_NAME, 'console-output'), successMsg))
        print('TASK COMPLETED for ', driver.current_url)
        driver.close()
    except TimeoutException:
        print('TimeoutException error : ', driver.current_url)


# FIND DIFFERENCE IN MINUTES  date_1 is from time, date_2 is to time
def differenceinminutes(date_1: object, date_2: object) -> object:
    time_delta = (date_2 - date_1)
    total_seconds = time_delta.total_seconds()
    minutes = total_seconds / 60
    print("diff in minutes >> ", minutes)
    return minutes


def test(driver, deployment, baseurl, tabindex, environment, globalActionEnabled, globalAction, sleepBeforeEachTabOpens):
    deployedconsolelinks = []
    service = 'pricing-order'
    print("service >> ", service)
    url = "https://jenkins.dp-dev.net/build?delay=0sec"
    deploy = "true"
    version = "2.0.0"
    action = "update"

    print("tab index " + str(tabindex) + " action " + action + " version " + str(version)
          + " url " + url + " deploy " + str(deploy))

    if deploy:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[tabindex])
        driver.get(url)
        select = Select(
            driver.find_element(By.XPATH, '//*[@id="main-panel"]/form/table/tbody[1]/tr[1]/td[3]/div/select'))
        select.select_by_visible_text(action)
        select = Select(
            driver.find_element(By.XPATH, '//*[@id="main-panel"]/form/table/tbody[2]/tr[1]/td[3]/div/select'))
        select.select_by_visible_text(service)

        ## docker version
        ##inputVersion = driver.find_element(By.XPATH,'//*[@id="main-panel"]/form/table/tbody[6]/tr[1]/td[3]/div/input[2]')

        ## eks version
        inputVersion = driver.find_element(By.XPATH,
                                           '//*[@id="main-panel"]/form/table/tbody[3]/tr[1]/td[3]/div/input[2]')
        inputVersion.clear()
        inputVersion.send_keys(version)
        driver.find_element(By.XPATH, '//*[@id="yui-gen1-button"]').click()
        print("Deployment Request submitted !")

        deployedHrefElement = driver.find_element(By.XPATH, '//*[@id="buildHistory"]/div[2]/table/tbody/tr[2]/td/div[1]/a')

        print("href >> " + deployedHrefElement.get_attribute('href'))
        deployedconsolelinks.append(baseurl + deployedHrefElement.get_attribute('href') + 'console')
        driver.get(baseurl + deployedHrefElement.get_attribute('href') + 'console')
        time.sleep(sleepBeforeEachTabOpens)