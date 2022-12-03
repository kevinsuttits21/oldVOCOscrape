# MODULES:
# this code does not work anymore due to code not efficiently scraping the table anymore, it gets the data but it is ordered oddly and you have to clean it by hand. Tried updating the code, but you have to still do it by hand in the end and it just isn't worth it.
from selenium import webdriver
from bs4 import BeautifulSoup
import re
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# open siseveeb login
url = 'https://siseveeb.voco.ee/kutseope/oppetoo/paevik/jooksvad_hinded'
driver.get(url)
# login credentials
my_username = 'XXXXXXXXX'# SET YOUR SISEVEEB NAME
my_password = 'XXXXXXXXX'# SET YOUR SISEVEEB PASSWORD, PREFERABLY IMPORT THE PASSWORD FROM AN OTHER FILE FOR SECURITY PURPOSES

# access login username input
username_input_box = driver.find_element(By.ID, "username")

# access login password input
password_input_box = driver.find_element(By.ID, "password")

# access login button
sign_in_button = driver.find_element(By.ID, "form_submit")

# clear the placeholders data
username_input_box.clear()
password_input_box.clear()

# fill login credentials
username_input_box.send_keys(my_username)
time.sleep(1)  # a 1-second time gap between filling username and password
password_input_box.send_keys(my_password)

time.sleep(2)  # a 2-second time delay

sign_in_button.click() # clicks the log in button
WebDriverWait(driver, 30)

driver.get('https://siseveeb.voco.ee/kutseope/oppetoo/paevik/jooksvad_hinded') # new driver source, start scraping after website

# get title info from table
source = driver.page_source
doc = BeautifulSoup(source, "html.parser")
tr_elements = doc.find_all('table')[0].find_all('tr') # get whole table raw data
# generate class names
keywordgen = doc.find_all('td', {'class' : 'font-bold footable-first-visible'}) # raw data for class names
l = re.findall('(</span>)(.*?)(</td>)', str(keywordgen))
i = 0
keyword = []
while i < len(l): # while loop to add class names to list
    keyword.append(l[i][1])
    i += 1
spans = doc.find_all('span', {'class' : 'footable-toggle fooicon fooicon-plus'})
lines = [span.get_text() for span in tr_elements] # get text AKA get titles and grades
# ignore first entry ([0]) in table (it is useless)
titles = [] # classes names in list
i = 0
j = 1
def remove_numbers(string):
  # Use a regular expression to match any digits in the string
  no_numbers = re.sub(r'\d+', '', string)
  # Return the resulting string
  return no_numbers

# Use a list comprehension to apply the remove_numbers function to each element in the list
lines2 = [remove_numbers(x) for x in lines]

# while loop that generates list of titles
while len(keyword) > i:
    if keyword[i] in lines2[j]:
        titles.append(keyword[i])
        i += 1
        j += 1
    else:
        j += 1

# grade titles ( ÕV - X )
span_elements = doc.find_all('table')[0].find_all('span') # raw data for ÕV titles
a = re.findall('(ÕV \w+ - )(.*?)(.;)', str(span_elements)) # raw data for titles regex
newlist = [] # list where we will place the cleaner lines
i = 0
# ÕV sentence generating and listing
for rida in a:
    if i < len(a):
        lauseke = a[i][0] + a[i][1] + a[i][2]
        newlist.append(lauseke)
        i += 1

# get ÕV grades
numberlist = []
spans2 = doc.find_all('span', {'class' : 'label label-info'})
regexime = re.findall('\>[\w]+\<', str(spans2)) # find the ÕV grades
i = 0
cleaner = [] # list of cleaned grades
# cleaned list of ÕV grades
while i < len(regexime):
    uus = regexime[i].replace(">", "")
    uus2 = uus.replace("<", "")
    cleaner.append(uus2)
    i += 1

# get overall grades
datavalueregex = re.findall('(<td class="footable-last-visible" data-sort-value=)(.*?)(.")', str(tr_elements)) # regex for getting the grades
# loop to clean up the raw data
i = 0
puhasnum = []
while i < len(datavalueregex):
    puhastus = datavalueregex[i][1] + datavalueregex[i][2]
    puhastus2 = puhastus.replace('"', '')
    puhasnum.append(puhastus2)
    i += 1

i = 0
print("Tulemused:")
# generation
while i < len(titles):
    print(titles[i])
    print(newlist[i] + "." + "\n" + "ÕV hinded: " + cleaner[i])
    print("Tavalised hinded: " + puhasnum[i])
    i += 1

# ending
time.sleep(8) # delays before exit
driver.close() # close the driver
