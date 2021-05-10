from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import json
import time

content=[]

driver = webdriver.Chrome('./drivers/chromedriver')
driver.maximize_window()
driver.get('https://www.adapt.io/login.htm?slc=web&login=true')

#login
email = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.NAME, 'emailSignIn'))
)
email.send_keys("masood.pg3200066@cloud.neduet.edu.pk")
driver.find_element_by_name("passwordSignin").send_keys("PyjGpKmF")
time.sleep(2)
driver.find_element_by_css_selector('.greenBut.form-submit.ng-binding').click()
time.sleep(5)

#read json file
data_frame = pd.read_json('./company_index.json', orient='records')
for index in range(0,len(data_frame)):
    contact_list=[]
    comp_name = data_frame.iloc[index]['company_name']
    comp_url = data_frame.iloc[index]['source_url']
    driver.get(comp_url)


    #find all Departments
    departments = driver.find_elements_by_css_selector('div.splitup.cp-landing > ul > li > a')

    #loop through all departments one by one
    for i in range(1,len(departments)+1):
        department = driver.find_element_by_css_selector('div.splitup.cp-landing > ul > li:nth-child('+str(i)+') > a')
        dpt_name = department.text
        department.click()
        time.sleep(2)

        employees = driver.find_elements_by_css_selector('.dept_contact_table[itemprop="employee"]')
        for employee in employees:
            contact={
                "contact_name": employee.find_element_by_css_selector('.dept_contact_name').text,
                "contact_email_domain": (employee.find_element_by_css_selector('.dept_email_phone.contact-action-wrapper > div:nth-child(1)').text).split('@')[1],
                "contact_jobtitle": employee.find_element_by_css_selector('.dept_contact_title').text,
                "contact_department": (dpt_name).split(' -')[0]
            }
            contact_list.append(contact)

        time.sleep(2)
        driver.execute_script("window.history.go(-1)")
        time.sleep(2)
    
    info = {
        "company_name": comp_name,
        "company_location": WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[itemprop="streetAddress"]'))).text,
        "company_website": (driver.find_element_by_css_selector('.data-web-address').text).replace('Web : ',''),
        "company_webdomain": (driver.find_element_by_css_selector('.data-web-address').text).replace('Web : http://www.', ''),
        "company_industry": driver.find_element_by_css_selector('div:nth-child(3) > p.address-info > span:nth-child(2)').text,
        "company_employee_size": driver.find_element_by_css_selector('div:nth-child(3) > p:nth-child(3) > span:nth-child(2)').text,
        "company_revenue": driver.find_element_by_css_selector('div:nth-child(3) > p:nth-child(2) > span:nth-child(2)').text,
        "contact_details": contact_list
    }

    content.append(info)
    print(content)


with open('./data/company_profiles.json', 'w') as fout:
    json.dump(content, fout, indent=0)



time.sleep(1)
driver.quit()