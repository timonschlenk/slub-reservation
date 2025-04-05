#import Selenium Libaries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Import the other libraries
import time
import json
import os

def generate_link(date, start_time, end_time, room_number = 20, level_number = 1):
    # Generate a link for the reservation page with the given date and time
    formated_start_time = start_time.replace(':', '%3A')
    formated_end_time = end_time.replace(':', '%3A')
    base_url = "https://raumbuchung.slub-dresden.de/Web/reservation/"
    return f"{base_url}?rid={room_number}&sid={level_number}&rd={date}&sd={date}{formated_start_time}&ed={date}{formated_end_time}"

LINK = generate_link('2025-04-25', '08:00', '09:00', 20, 1) # Generate the link for the reservation page

# Setup Chrome options and service
service = Service(executable_path='./chromedriver.exe')
driver = webdriver.Chrome(service=service)

# Load credentials from config file using a relative path
config_path = os.path.join(os.path.dirname(__file__), './config.json')
with open(config_path, 'r') as config_file:
    config = json.load(config_file)

USERNAME = config['username']
PASSWORD = config['password']

#Execute the script
driver.get(LINK) # Open the reservation page
SubmitButton = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, 'btn-large'))
) # Wait for the submit button to be clickable
SubmitButton.click() # Click the submit button

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, 'body'))
)

UsernameInput = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'txtUsername'))
) # Wait for the username input field to be present

PasswordInput = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'txtPassword'))
) # Wait for the password input field to be present 

SubmitButton = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'btnLogin'))
) # Wait for the submit button to be present

UsernameInput.send_keys(USERNAME) # Enter the username
PasswordInput.send_keys(PASSWORD) # Enter the password
SubmitButton.click() # Click the submit button
# Wait for 5 seconds
time.sleep(10)

# Close the browser
driver.quit()