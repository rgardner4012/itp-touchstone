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
# Setup the dataframes for each school
school_dfs = { k: pd.DataFrame( columns=["WGU_Class","Credits", f"{k}"]) for k in school_set }

# Setup the Chrome driver options, and configure the driver
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

# Get the page at the given URL
def get_url(url):
  driver.get(url)
  return driver

# Get the table data from the page
def get_table_data(school, table, df):
  # ingest table data, read rows, read each cell, build a list of lists with the row/data, then add to the dataframe.
  table_body = driver.find_element(By.XPATH, table)
  table_rows = table_body.find_elements(By.TAG_NAME, "tr")
  all_rows = []
  for row in table_rows:
    table_data = row.find_elements(By.TAG_NAME, "td")
    row_data =  []
    for data in table_data:
      row_data.append(data.text)
    all_rows.append(row_data)
  new_df = pd.DataFrame(all_rows, columns=["WGU_Class", "Credits", f"{school}"])
  df = pd.concat([df, new_df], ignore_index=True)
  return df

# Get the data from the page and add it to the school_data dictionary to seperate the data by school
def get_school_data(school="all"):
  school_data = {}
  if school == "all":
    all_results = pd.DataFrame(columns=["WGU_Class", "Credits"])
    for school in school_set:
      school_page = get_url(url_set[school])
      for table in school_tables[school].values():
        school_dfs[school] = get_table_data(school, table, school_dfs[school])
    for school in school_dfs.keys():
      all_results = pd.merge(school_dfs[school], all_results, on=["WGU_Class", "Credits"], how="outer")
    return all_results
  else:
    df = pd.DataFrame(columns=["WGU_Class", "Credits", f"{school}"])
    print("School: ", school)
    school_page = get_url(url_set[school])
    for table in school_tables[school].values():
      school_dfs[school] = get_table_data(school, table, school_dfs[school])
  return school_dfs

# Select the school(s) you're interested in transferring credits from
def school_selection():
  print("Select school(s) your interested in transferring credits from")
  options = ["all", "sophia", "studycom", "saylor"]
  selection = Prompt.menu(options)
  return selection

# Get the schools the user is interested in
school_sel = school_selection()

print(school_sel) # Debugging, left in for clarity
# Get the data for the selected school(s) into the results dataframe
results = get_school_data(school_sel)
# branching for all vs specific school
if school_sel == "all":
  print(results)
  with open("output.csv", "w") as file:
    results.to_csv(file)
else:
  print(results[school_sel])
  with open("output.csv", "w") as file:
    results[school_sel].to_csv(file)

# Close the driver
driver.quit()


