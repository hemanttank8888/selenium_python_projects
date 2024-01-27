from telnetlib import EC
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
uc.TARGET_VERSION = 85
driver = uc.Chrome(options=options)
options.add_experimental_option("detach", True)
    
stock_symbols = ["XEL","SIRI", "RIVN", "CEG", "TMUS", "CHTR", "AEP", "KDP", "PEP", "AZN", "FI", "HON", "GILD", "EXC", "CMCSA", "VRSK", "WBA", "FAST", "MDLZ", "VRTX", "FANG", "ODFL", "KHC", "JD", "DLTR", "MAR", "CTAS", "MNST", "REGN", "COST", "AMGN", "PAYX", "EA", "ATVI", "ADP", "CSCO", "ABNB", "ILMN", "PCAR", "CSX", "MRNA", "BKNG", "ROST", "SGEN", "EBAY", "MU", "PDD", "ISRG", "BIIB", "IDXX", "SBUX", "AAPL", "CPRT", "ORLY", "SNPS", "FTNT", "WBD", "AVGO", "CSGP", "CDNS", "BKR", "PANW", "PYPL", "INTU", "ADBE", "TXN", "LULU", "DXCM", "MELI", "MSFT", "GOOGL", "ANSS", "GOOG", "QCOM", "ADI", "INTC", "NVDA", "CTSH", "ALGN", "GFS", "MRVL", "ADSK", "NXPI", "MCHP", "LRCX", "AMZN", "WDAY", "META", "KLAC", "LCID", "DDOG", "ENPH", "AMD", "AMAT", "ASML", "ZM", "CRWD", "TEAM", "ZS", "NFLX", "TSLA"]

for symbol in stock_symbols:
    driver.get(f"https://thefly.com/news.php?symbol={symbol}")
    scroll=True
    count=0
    while scroll:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.7+count)
        current_date = datetime.now().strftime("%Y-%m-%d")
        previous_day = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")        
        all_today = driver.find_elements(By.XPATH, f"//tr[starts-with(@data-datenews,'{current_date}')]/td[2]//div[@class='story_header']/a")
        all_yesterday= driver.find_elements(By.XPATH, f"//tr[starts-with(@data-datenews,'{previous_day}')]/td[2]//div[@class='story_header']/a")
        all_heading=all_today+all_yesterday
        count+=1
        try:
            xpath_expression = "//div[@class='newsFeedWidget feedCerrado']//table[last()-1]//tr[last()]"
            matching_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, xpath_expression))
            )
            dates = [element.get_attribute('data-datenews').split(" ")[0] for element in matching_elements]
            date_to_compare = datetime.strptime(dates[0], "%Y-%m-%d")
            date_to_compare_string = date_to_compare.strftime("%Y-%m-%d")
            date_to_compare = datetime.strptime(date_to_compare_string, "%Y-%m-%d")
            previous_day_datetime = datetime.strptime(previous_day, "%Y-%m-%d")
            if date_to_compare < previous_day_datetime:
                print("false")
                scroll = False
            if count>3 and len(all_heading)<(count*50)+10:
                scroll = False
        except:
            continue
    urls = [url.get_attribute("href") for url in all_heading]
    for url in urls:
        print(symbol)
        driver.get(url)
        try:
            about_element = driver.find_element(By.XPATH, "//div[@id='onTheFlyNewLanding']").text.replace("\n", "").replace("\t", "").strip()
            name_file=url.split("id")[1].split("/")[0]
            with open(f"D:\All_Selenium_Projects\output\{symbol}fly{name_file}.txt", "w") as f:
                f.write(about_element)
        except:
            about_element=""


        print(about_element)
driver.quit()
