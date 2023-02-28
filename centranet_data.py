import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://hk.centanet.com/findproperty/en/list/transaction")
def capitalize(words):
    words= words.split()
    for i in range(len(words)):
        words[i] = words[i].capitalize()
    words = ' '.join(words)
    return words
wait = WebDriverWait(driver, 10)
inputElem = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "input")))
inputElem.clear()
print('Enter property name:')
propertys = input()
propertys = capitalize(propertys)
print('Enter Sold/Leased:')
sold_leased = input()
sold_leased = capitalize(sold_leased)
inputElem.send_keys(propertys)
wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-search"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn-fiter']/span[contains(text(), 'Sold / Leased')]"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='el-radio__label']/span[contains(text(), '%s')]"%sold_leased))).click()
click_next = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-next")))

def extract_data(element):
    columns = element.find_elements(By.CSS_SELECTOR,"div[class*='bx--structured-list-td']")
    Date = columns[0].text
    Dev = columns[1].text
    Price = columns[3].text
    RiseBox = columns[4].text
    Area = columns[5].text
    return{
       "Date": Date,
       "Development": Dev,
       "Consideration": Price,
       "Change": RiseBox,
       "Area": Area
         }

data = []

while True:
    time.sleep(2)
    contents = driver.find_element(By.CSS_SELECTOR,"div[class*='bx--structured-list-tbody']")
    properties = contents.find_elements(By.CSS_SELECTOR,"div[class*='bx--structured-list-row']")
    for propert in properties:
        extracted_data = extract_data(propert)
        data.append(extracted_data)
    if click_next.is_enabled():
        click_next.click()
    else:
        break #break the while loop if click next is disable
    time.sleep(2)
driver.quit()
df = pd.DataFrame(data)
df.to_csv("result.csv", index=False)
print(df)