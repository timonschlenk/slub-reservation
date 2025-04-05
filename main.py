#import Selenium Libaries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Import the time library
import time

# Setup Chrome options and service
service = Service(executable_path='./chromedriver.exe')
driver = webdriver.Chrome(service=service)

#Execute the script
driver.get('https://www.dhsz.tu-dresden.de/angebote/aktueller_zeitraum/_Doppelkopf.html') # Open the Doppelkopf page

# # Wait for the link to be present on the page
# link_to_inscription = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.LINK_TEXT, 'buchen')) # ID of the link
# )

# Wait for the link to be present on the page
link_to_inscription = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.LINK_TEXT, 'Jonas Kunigkeit')) # ID of the link
)

link_to_inscription.click()

# Wait for 5 seconds
time.sleep(5)

# Close the browser
driver.quit()