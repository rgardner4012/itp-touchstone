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
#from consolemenu import *
#from consolemenu.items import *
from simple_term_menu import TerminalMenu
from prompt import Prompt
import pandas as pd

# Setup necessary data (URLs, XPaths, etc.)
school_set = ["sophia", "studycom", "saylor"]
url_set = { 
  "sophia": "https://partners.wgu.edu/transfer-pathway-agreement?uniqueId=BSCS7110&collegeCode=IT&instId=796&programId=37",
  "studycom": "https://partners.wgu.edu/transfer-pathway-agreement?uniqueId=BSCS4424&collegeCode=IT&instId=678&programId=37",
  "saylor": "https://partners.wgu.edu/transfer-pathway-agreement?uniqueId=BSCS671&collegeCode=IT&instId=186&programId=37",
}
school_tables = {
  "sophia": {
    "WGU General Ed Courses": '//*[@id="pageContent"]/span/span/builder-content/builder-blocks/div/div/builder-component-element/div/div/div/div/div/div/div[3]/div/div/div[2]/div/div/div/div/div/div/div[2]/wgu-tpa-table/table[1]/tbody',
    "WGU Additional Courses": '//*[@id="pageContent"]/span/span/builder-content/builder-blocks/div/div/builder-component-element/div/div/div/div/div/div/div[3]/div/div/div[2]/div/div/div/div/div/div/div[2]/wgu-tpa-table/table[2]/tbody',
  },
  "studycom": {
    "WGU General Ed Courses": '//*[@id="pageContent"]/span/span/builder-content/builder-blocks/div/div/builder-component-element/div/div/div/div/div/div/div[3]/div/div/div[2]/div/div/div/div/div/div/div[2]/wgu-tpa-table/table[1]/tbody',
    "WGU Additional Courses": '//*[@id="pageContent"]/span/span/builder-content/builder-blocks/div/div/builder-component-element/div/div/div/div/div/div/div[3]/div/div/div[2]/div/div/div/div/div/div/div[2]/wgu-tpa-table/table[2]/tbody',
  },
  "saylor": {
    "WGU General Ed Courses": '//*[@id="pageContent"]/span/span/builder-content/builder-blocks/div/div/builder-component-element/div/div/div/div/div/div/div[3]/div/div/div[2]/div/div/div/div/div/div/div[2]/wgu-tpa-table/table[1]/tbody',
    "WGU Additional Courses": '//*[@id="pageContent"]/span/span/builder-content/builder-blocks/div/div/builder-component-element/div/div/div/div/div/div/div[3]/div/div/div[2]/div/div/div/div/div/div/div[2]/wgu-tpa-table/table[2]/tbody',
  },
}
school_dfs = { k: pd.DataFrame( columns=["WGU_Class","Credits","transferable"]) for k in school_set }
#print(school_dfs)
#   "sophia": pd.DataFrame(columns=["WGU_Class","Credits","transferable"]),
#   "studycom": pd.DataFrame(columns=["WGU_Class","Credits","transferable"]),
#   "saylor": pd.DataFrame(columns=["WGU_Class","Credits","transferable"]),
# }
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

# driver = webdriver.Chrome(ChromeDriverManager().install())


# # Moved temporarily
#   with open("output.csv", "w") as file:
#   writer = csv.writer(file)

# Get the page at the given URL
def get_url(url):
  driver.get(url)
  return driver

# Get the table data from the page
def get_table_data(table, df):
  table_body = driver.find_element(By.XPATH, table)
  table_rows = table_body.find_elements(By.TAG_NAME, "tr")
  all_rows = []
  for row in table_rows:
    table_data = row.find_elements(By.TAG_NAME, "td")
    row_data =  []
    for data in table_data:
      row_data.append(data.text)
    all_rows.append(row_data)
  #print("All Rows: ", all_rows) 
  new_df = pd.DataFrame(all_rows, columns=["WGU_Class","Credits","transferable"])
  df = pd.concat([df, new_df], ignore_index=True)
  #df = df._append(new_df, ignore_index=True)
  #print(df)
  return df

# Get the data from the page and add it to the school_data dictionary
def get_school_data(school="all"):
  school_data = {}
  if school == "all":
    for school in url_set.keys():
      school_page = get_url(url_set[school])
      for table in f"{school}_tables":
        school_data == pd.concat(get_table_data(table, school_data[school]))
  else:
    df = pd.DataFrame(columns=["WGU_Class","Credits","transferable"])
    print("School: ", school)
    school_page = get_url(url_set[school])
    for table in school_tables[school].values():
      #print("Table: ", table, "from school: ", school, "tables: ", school_tables[school])
      school_dfs[school] = get_table_data(table, school_dfs[school])
  #school_data[school] = get_table_data(table, school_dfs[school])
  return school_dfs
# Build a list of classes from the given school, Any school should work as all classes should be the same      
# def build_class_list(school="sophia"):
#   class_list = []
  
#   resp = get_url(url_set[school])
#   tables = sophia_tables if school == "sophia" else studycom_tables if school == "studycom" else saylor_tables
#   for table in tables:
#     get_table_data(table)
#     class_list.append((school, table))
#   return class_list

# Select the school(s) you're interested in transferring credits from
def school_selection():
  print("Select school(s) your interested in transferring credits from")
  options = ["all", "sophia", "studycom", "saylor"]
  #options = ["All", "WGU General Ed Courses", "WGU Core Courses", "WGU Additional Courses"]
  selection = Prompt.menu(options)
  return selection


school_sel = school_selection()
print(school_sel)
results = get_school_data(school_sel)
print(results[school_sel])
driver.quit()

  # tables = sophia_tables if school == "sophia" else studycom_tables if school == "studycom" else saylor_tables if school == "saylor" else 
  # for table in tables:
  #   print(table)


  #   driver.get(url)
  #   table_body = driver.find_element(By.XPATH, table)
  #   table_rows = table_body.find_elements(By.TAG_NAME, "tr")
  #   with open("output.csv", "w") as file:
  #     writer = csv.writer(file)
  #     for row in table_rows:
  #       table_data = row.find_elements(By.TAG_NAME, "td")
  #       row_data =  []
  #       for data in table_data:
  #         row_data.append(data.text)
  #       writer.writerow(row_data)
  #   driver.quit()


# options = Options()
# options.add_argument('--no-sandbox')
# options.add_argument('--headless')
# options.add_argument('--disable-dev-shm-usage')

# options.add_argument("start-maximized"); 
# options.add_argument("disable-infobars"); 
# options.add_argument("--disable-extensions"); 
# options.add_argument("--disable-gpu"); 
# options.add_argument("--disable-dev-shm-usage"); 

# driver = webdriver.Chrome(options=options)
# driver.implicitly_wait(5)

# driver.get(url)
# table_body = driver.find_element(By.XPATH, '/html/body/app-root/div/builder-component[2]/span/span/builder-content/builder-blocks/div/div/builder-component-element/div/div/div/div/div/div/div[3]/div/div/div[2]/div/div/div/div/div/div/div[2]/wgu-tpa-table/table[1]/tbody')
# table_rows = table_body.find_elements(By.TAG_NAME, "tr")
# with open("output.csv", "w") as file:
#   writer = csv.writer(file)
  
#   for row in table_rows:
#     table_data = row.find_elements(By.TAG_NAME, "td")
#     row_data =  []
#     for data in table_data:
#       row_data.append(data.text)
#     writer.writerow(row_data)
    


