# NFL Stats scraper
# Author: Jameel Kaba

# Import statements
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import pandas as pd

# User input for category and year
statisticCategory = input("Which statistical category (rushing/passing):")
season = input("For which year: ")

# Datset could have multiple pages.  We will start on page 1 to begin
p = 1

payload = {"statisticCategory":statisticCategory.upper(),"seasonType":"REG","d-447263-p":str(p),"season":season}
url = 'http://www.nfl.com/stats/categorystats'
response = requests.get(url,params=payload)

# Print response, 200 means it went through
print("Response:", response.status_code,response.url) 

soup = BeautifulSoup(response.text,'html.parser')

# The website table is partitioned into multiple pages.  We need to know how many pages to iterate
pagingText = soup.find("span", {"class": "linkNavigation floatRight"})
pagingLinks = pagingText.findAll("a")
pages = len(pagingLinks)
print("Number of page links:",len(pagingLinks))

# Get Header for the table
columnHeader = []
header = soup.find('table', attrs={'id':'result'}).find_all('th')
for c in header:
    columnHeader.append(c.text)
columnHeader = [c.strip('\n') for c in columnHeader]

tableRows = []

for pg in range(1,pages+1):
    
    # Pause our code for a second so that we are not spamming the website with requests. 
    # This helps us avoid getting flagged as a spammer.
    time.sleep(1)
    
    # Update page number in payload
    payload["d-447263-p"] = pg
    response = requests.get(url,params=payload)
    print("Page:",pg,"url:",response.url)
    soup = BeautifulSoup(response.text,'html.parser')
    table = soup.find('table', attrs={'id':'result'})
    rows = table.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        if cols:
            cols = [ele.text.strip() for ele in cols]
            tableRows.append([ele for ele in cols if ele]) # Get rid of empty values

resultsDF = pd.DataFrame(tableRows, columns=columnHeader)
display(resultsDF.head(),resultsDF.shape)

# Save results to Excel
baseFileName = "NFL_Stats"
resultsDF.to_excel(baseFileName + statisticCategory + "_" + season + ".xlsx",index=False)