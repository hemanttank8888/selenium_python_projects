import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
from lxml import etree
import csv
import pandas as pd

def write_output(data,dpBloodGroup,dpState):
    dpState = dpState.replace(' ','').replace('_','')
    get_data_datafram = pd.DataFrame(data)
    get_data_datafram.to_csv(f"{dpState}__{dpBloodGroup}.csv")

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())

bloodGroup = ["A2B-","AB+","AB-"]

for dpBloodGroup in bloodGroup:
    driver.get("https://www.friends2support.org/")
    time.sleep(1)
    bloodGroup = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.XPATH, f"//select[@id='dpBloodGroup']//option[@value='{dpBloodGroup}']")))
    bloodGroup.click()
    time.sleep(1)

    try:
        time.sleep(1)
        Country = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.XPATH, f"//select[contains(@id,'dpCountry')]/option[2]")))
        dpCountry = Country.text
    except:
        Country = None
    if Country:
        Country.click()
    else:
        break
    time.sleep(1)

    datas = []
    for i in range(2,100):
        try:
            time.sleep(1)
            State = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.XPATH, f"//select[@id='dpState']/option[{i}]")))
            dpState = State.text
        except:
            State = None
        if State:
            State.click()
        else:
            break
        time.sleep(1)
        for i in range(2,100):
            try:
                time.sleep(1)
                Dist = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.XPATH, f"//select[@id='dpDistrict']/option[{i}]")))
                district = Dist.text
            except:
                Dist = None
            if Dist:
                Dist.click()
            else:
                break
            time.sleep(1)
            for i in range(2,100):
                try:
                    time.sleep(1)
                    City = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.XPATH, f"//select[@id='dpCity']/option[{i}]")))
                    selected_City = City.text
                except:
                    City = None
                if City:
                    City.click()
                else:
                    break
                time.sleep(1)
                Search = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.XPATH, "//input[@id='btnSearchDonor']")))
                Search.click()

                count =1
                def fetch_data(count):

                    while True:
                        page_souece = driver.page_source
                        soup = BeautifulSoup(page_souece, 'html.parser')
                        tree = etree.HTML(str(soup))
                        selected_elements = tree.xpath("//tr[contains(@style,'background-color')]")
                        for element in selected_elements:
                            row_data = {}
                            name = ''.join(element.xpath(".//span[contains(@id,'blFullName_')]/text()"))
                            satus_of = ''.join(element.xpath(".//span[contains(@id,'AvailUnavail')]//text()"))
                            MobileNumber = ''.join(element.xpath(".//span[contains(@id,'MobileNumber')]//text()"))
                            row_data['name'] = name
                            row_data['satus_of'] = satus_of
                            row_data['MobileNumber'] = MobileNumber
                            row_data['dpBloodGroup'] = dpBloodGroup
                            row_data['dpCountry'] = dpCountry
                            row_data['dpState'] = dpState
                            row_data['dpDistrict'] = district
                            row_data['dpCity'] = selected_City
                            if row_data['name'] != "":
                                datas.append(row_data)
                                print(row_data,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                        try:
                            next_page= element.xpath('//tbody/tr[1]/td/span/following-sibling::a[1]/@href')
                            if next_page:
                                count +=1
                                next_pagenation  =  ''.join(element.xpath('//tbody/tr[1]/td/span/following-sibling::a[1]/@href'))
                                driver.execute_script(next_pagenation)
                                print(next_pagenation,"#####245356..156.56.53689")

                                time.sleep(2)
                                return fetch_data(count)
                            else:
                                break
                        except: 
                            break

                fetch_data(count)
        write_output(datas,dpBloodGroup,dpState)
        datas = []

    