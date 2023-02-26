from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import datetime as dt
import pandas as pd

#open chrome web browser
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://hk.centanet.com/findproperty/en/list/transaction")

#Input address and select sold/lease
wait = WebDriverWait(driver, 10)
inputElem = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "input")))
inputElem.clear()
inputElem.send_keys('Discovery Park')
wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-search"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn-fiter']/span[contains(text(), 'Sold / Leased')]"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='el-radio__label']/span[contains(text(), 'Sold')]"))).click()
click_next = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-next")))

#put element to lst
Date=Address=Price=Changes=Saleable_Area=[]
def it(x):
    lst=[]
    for i in x:
        lst.append(i.text)
    return lst

#find elements in web page
while True:
    content = driver.find_element(By.CSS_SELECTOR, "#__layout .bx--structured-list")
    info_date = content.find_elements(By.CLASS_NAME,"info-date")
    Date = Date + it(info_date)
    info_address = content.find_elements(By.XPATH, "//div[@class='cv-structured-list-data bx--structured-list-td']/div[contains(text(), 'Discovery Park')]")
    Address = Address + it(info_address)
    tranprice = content.find_elements(By.CLASS_NAME,"tranPrice")
    Price = Price + it(tranprice)
    info_changes = content.find_elements(By.CLASS_NAME,"riseBox")
    Changes = Changes + it(info_changes)
    feet = content.find_elements(By.XPATH, "//div[@class='cv-structured-list-data bx--structured-list-td']/div[contains(text(), 'ft²')]")
    Saleable_Area = Saleable_Area + it(feet)
    if click_next.is_enabled():
        click_next.click()
    else:
        break #break the while loop if click next is disable
    sleep(2)
driver.quit()
    
    
#put data to csv
df = pd.DataFrame()
df['Date'] = Date
df['Address'] = Address
df['Price'] = Price
df['Changes%'] = Changes
df['Saleable_Area'] = Saleable_Area
df.to_csv("result.csv", index=False)

