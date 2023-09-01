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
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm

def find_src_attributes(text):
    src_pattern = re.compile(r'src="([^"]+)"')
    matches = re.findall(src_pattern, text)
    return matches

def find_href_attributes(text):
    href_pattern = re.compile(r'href="([^"]+)"')
    matches = re.findall(href_pattern, text)
    return matches

def find_title_attributes(text):
    if text is None:
        return ''
    href_pattern = re.compile(r'tle">(.*?)<')
    matches = re.search(href_pattern, text).group(1)
    return matches

def find_date_attributes(text):
    if text is None:
        return ''
    href_pattern = re.compile(r'\d{4}年\d{2}月\d{2}日 \d{2}:\d{2}')
    matches = re.search(href_pattern, text).group()
    return matches

sql_commands = """
/*
Navicat MySQL Data Transfer

Source Server         : leadnews
Source Server Version : 50724
Source Host           : localhost:3306
Source Database       : leadnews

Target Server Type    : MYSQL
Target Server Version : 50724
File Encoding         : 65001

Date: 2023-08-29 10:08:24
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for eastmoneyarticles
-- ----------------------------
DROP TABLE IF EXISTS `eastmoneyarticles`;
CREATE TABLE `eastmoneyarticles` (
  `id` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `content` varchar(10000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `imageurl` varchar(5000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `createtime` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

"""


# Open the file for reading
with open( "eastmoneypageurlleft.txt", "r") as file:
    urlList = file.readlines()  # Read all lines from the file

# Remove newline characters and leading/trailing whitespaces
urlList = [url.strip() for url in urlList]
# urlList = sorted(urlList)
# print(len(urlList))

i = 0
j = 0
total_pages = len(urlList)
if total_pages == 11378:
    with open('eastmoneyarticles.sql', 'w') as sql_file:
        sql_file.write(sql_commands)
    sql_commands = ''
# Create a tqdm progress bar
progress_bar = tqdm(total=total_pages, unit="page", dynamic_ncols=True)
for i in range(total_pages):
    url = urlList[i]
    # Update the progress bar description
    progress_bar.set_description(f"#{i + 1} ({j} failed) {url}")
    # Update the progress bar value
    progress_bar.update(1)

    try:
        # Your scraping code that might raise WebDriverException
        # Set up Chrome options for headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        # print(url)
        # Create a WebDriver instance
        driver = webdriver.Chrome(options=chrome_options)
        
        # Load a web page
        driver.get(url)

        # Wait for a specific element to be present (timeout of 30 seconds)
        wait = WebDriverWait(driver, 120)
        element = wait.until(EC.presence_of_element_located((By.ID, "ContentBody")))

        # Get the page source after the dynamic content has loaded
        response = driver.page_source

        # Close the browser
        driver.quit()
        
    except WebDriverException as e:
        print(f"An exception occurred while scraping {url}: {e}")
        # Continue to the next URL
        with open('eastmoneypageurlfailed.txt', 'a') as failedurl:
            failedurl.write(url)
        j += 1
        i += 1
        continue
    
    try:
        id = re.search(r'\d+', url).group()
        # print(id)
        # print(url)
            
        # Check if the request was successful
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response, 'html.parser')

        # Find title
        topbox = soup.find('div', id='topbox')
        title = str(find_title_attributes(str(topbox)))
        # print(title)
        createtime = str(find_date_attributes(str(topbox)))
        # print(createtime)
        contentBody = soup.find('div', id='ContentBody')
        article = contentBody.get_text()
        # print(article)
        image = str(find_src_attributes(str(contentBody)))
        # print(image)  
        # print('#'+ str(i) + ' ' + url + ' complete')
        sql_commands = f"""INSERT INTO eastmoneyarticles VALUES ("{str(id)}", "{title}", "{article}", "{image}", "{url}", "{createtime}");\n"""

        # Append the SQL commands to a .sql file
        with open('eastmoneyarticles.sql', 'a') as sql_file:
            sql_file.write(sql_commands)
        sql_commands = ''

        # Remove the finished line
        urlListn = urlList[i+1:]
        # print(urlListn)
        # Write new lines to output file
        with open('eastmoneypageurlleft.txt', "w") as f:
            for urlL in urlListn:
                    f.write(urlL + '\n')

    except Exception as e:
        print(f"An error occurred: {e}")
        with open('eastmoneypageurlfailed.txt', 'a') as failedurl:
            failedurl.write(url)
        j += 1
        i += 1
        continue
    i += 1





