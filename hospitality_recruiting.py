import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
from lxml import etree
import csv
import pandas as pd


driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
driver.get("https://www.hospitalrecruiting.com/")
all_heading = driver.find_elements(By.XPATH, "//select[1]//option[starts-with(@class,'dropdown')]")
all_data=[]

for speciality in all_heading:
    time.sleep(2)
    # speciality = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.XPATH, f"//select[1]//option[{i}]")))
    speciality.click()
    
    for i in range(53,55):
        time.sleep(1)
        location = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.XPATH, f"//select[2]//option[{i}]")))
        location.click()
        location_t = location.text
        search = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.XPATH, f"//form[@name='search_1']//input[1]")))
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).click(search).key_up(Keys.CONTROL).perform()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(4)
        
        def next_page_func():
            all_job = driver.find_elements(By.XPATH, "//span[@class='action']/a[@class='btn green small radius floatleft']")
            data={}
            for i in all_job:
                href = i.get_attribute('href')
                print(href)
                actions = ActionChains(driver)
                actions.key_down(Keys.CONTROL).click(i).key_up(Keys.CONTROL).perform()
                time.sleep(2)
                driver.switch_to.window(driver.window_handles[2])
                time.sleep(2)
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                tree = etree.HTML(str(soup))
                tee = ''.join(tree.xpath("./html"))

                title = ''.join(tree.xpath(".//h1/text()"))
                company = ''.join(tree.xpath(".//div[@id='main_container']//div[@id='job_details_container']/span[1]/span[2]/a[1]/text()"))
                profassion = ''.join(tree.xpath(".//div[@id='main_container']//div[@id='job_details_container']/span[2]/span[2]/a[1]/text()"))
                Location = ''.join(tree.xpath(".//div[@id='main_container']//div[@id='job_details_container']/span[3]/span[2]/span[1]/text()"))
                Job_Type = ''.join(tree.xpath(".//div[@id='main_container']//div[@id='job_details_container']/span[4]/span[2]/text()")).strip()
                try:
                    discription=driver.find_element(By.XPATH,"//div[@class='text_block job_description job_description_content_container  add_scrollbar']").text
                except:
                    discription=None
                try:
                    about=driver.find_element(By.XPATH,"//div[@id='text_block_org']").text
                except:
                    about=None
                data['Domain']='hospitalrecruiting.com'
                data['href']=href
                data['about']=about
                data['discription']=discription
                data['company']=company
                data['profassion']=profassion
                data['Location']=Location
                data['Job_Type']=Job_Type
                all_data.append(data)
                data={}
                
                driver.close()
                driver.switch_to.window(driver.window_handles[1])
            
            
            try:
                next_page=driver.find_element(By.XPATH, "//div[@class='hide-mobile']/a[@class='next page-numbers']")
                if next_page:
                    next_page.click()
                    time.sleep(2)
                    next_page_func()
            except:
                pass
            
        next_page_func()  
         
        time.sleep(3)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(2)
get_data_datafram = pd.DataFrame(all_data)
get_data_datafram.to_csv("hospital_recruting.csv")


driver.quit()
