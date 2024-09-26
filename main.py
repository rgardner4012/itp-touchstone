from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup as bs
import csv

# Chrome driver path in replit?
#chrome_driver_path = ""
#driver = webdriver.Chrome(ChromeDriverManager().install())
#driver.maximize_window()

# URL of the website to scrape
url = "https://partners.wgu.edu/transfer-pathway-agreement?uniqueId=BSCS7110&collegeCode=IT&instId=796&programId=37"

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')

options.add_argument("start-maximized"); 
options.add_argument("disable-infobars"); 
options.add_argument("--disable-extensions"); 
options.add_argument("--disable-gpu"); 
options.add_argument("--disable-dev-shm-usage"); 

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)

driver.get(url)
table_body = driver.find_element(By.XPATH, '/html/body/app-root/div/builder-component[2]/span/span/builder-content/builder-blocks/div/div/builder-component-element/div/div/div/div/div/div/div[3]/div/div/div[2]/div/div/div/div/div/div/div[2]/wgu-tpa-table/table[1]/tbody')
table_rows = table_body.find_elements(By.TAG_NAME, "tr")
with open("output.csv", "w") as file:
  writer = csv.writer(file)
  
  for row in table_rows:
    table_data = row.find_elements(By.TAG_NAME, "td")
    row_data =  []
    for data in table_data:
      row_data.append(data.text)
    writer.writerow(row_data)
    
driver.quit()

