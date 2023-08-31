import requests
import re
import datetime
import time
from datetime import timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def find_href_attributes(text):
    href_pattern = re.compile(r'href="([^"]+)"')
    matches = re.findall(href_pattern, text)
    return matches

# Get all pages url
urlpages = [
# "https://finance.eastmoney.com/a/cgspl.html",
# "https://finance.eastmoney.com/a/ccyts.html",
# "https://finance.eastmoney.com/a/cjjsp.html",
# "https://finance.eastmoney.com/a/csygc.html",
# "https://finance.eastmoney.com/a/cgspl.html", 
# "https://finance.eastmoney.com/a/ccjdd.html",
# "https://finance.eastmoney.com/a/ccjxw.html",
# "https://finance.eastmoney.com/a/cgnjj.html",
# "https://finance.eastmoney.com/a/cgjjj.html",
# "https://finance.eastmoney.com/a/czqyw.html",
# #41
# "https://finance.eastmoney.com/a/czsdc.html",
# "https://hk.eastmoney.com/a/cgsbd.html",
# "https://stock.eastmoney.com/a/cmgpj.html",
# "https://finance.eastmoney.com/a/cssgs.html"
]


urlList = []
tempurl = ""
for urlpage in urlpages:
    i = 1
    while i < 51:
        if i != 1:
            tempurl = "_" + str(i) + ".ht"
            tempurl = urlpage.replace(".ht",tempurl)
        else:
            tempurl = urlpage
        print(tempurl)
        # Set up Chrome options for headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode

        # Create a WebDriver instance
        driver = webdriver.Chrome(options=chrome_options)

        # Load a web page
        driver.get(tempurl)
        
        # Wait for a specific element to be present (timeout of 30 seconds)
        wait = WebDriverWait(driver, 30)
        element = wait.until(EC.presence_of_element_located((By.ID, "newsListContent")))
        
        # Get the page source after the dynamic content has loaded
        response = driver.page_source
        
        # Close the browser
        driver.quit()
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response, 'html.parser')

        tempList = soup.find_all('li',id=re.compile("^newsTr"))
        # print(tempList)
        newsList = []
        
        for item in find_href_attributes(str(tempList)):
            if item not in newsList:
                newsList.append(item)
        # print(newsList)
        # urlList.extend(newsList)
        # print(len(urlList))
        with open('eastmoneypageurl.txt', 'a') as pageurl_file:
            for news in newsList:
                pageurl_file.write(news + '\n')

        i += 1
