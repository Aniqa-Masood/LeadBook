from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json
import time

driver = webdriver.Chrome('./drivers/chromedriver')
driver.maximize_window()
driver.get('https://www.adapt.io/directory/industry/telecommunications/A-1')

content=[]

def close_popup():
    try:
        popup = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.CookiePolicyBanner_closeIcon__1_fa5'))
        )
        popup.click()
    except:
        print('no popup')

def work():
    time.sleep(5)
    #loop through company name and url
    for i in driver.find_elements_by_css_selector(".DirectoryList_seoDirectoryList__aMaj8 > .DirectoryList_linkItemWrapper__3F2UE > a"):
        info = {
            "company_name": i.text,
            "source_url": i.get_attribute("href")
        }
        #append dictionary in list
        content.append(info)


#-------------------Work Start from here------------------------

for alphabet in range(1,27):
    #Click on alphabet
    driver.find_element_by_css_selector('.DirectoryTopInfo_alphabetLinkListWrapper__4a1SM > div:nth-child('+str(alphabet)+')').click()

    #Close Pop-up if exixts
    close_popup()

    #Click on next button and copy data until next button exists
    while True:
        try:
            #find all company names in that page
            work()

            #Click on next button if exixts and then copy data of next page ,otherwise break loop and click on next alphabet
            next_page = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.DirectoryList_actionBtnLink__Seqhh.undefined > a'))
            )
            next_page.click()

        except TimeoutException:
            break


#Save this list of dictionaries to file named company_index.json
with open('./data/company_index.json', 'w') as fout:
    json.dump(content, fout, indent=0)

time.sleep(1)
driver.quit()