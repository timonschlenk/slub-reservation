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

DATE = '2025-04-19' # Date for the reservation
START_TIME = '19:00' # Start time for the reservation
END_TIME = '20:00' # End time for the reservation
ROOM_NUMBER = 20 # Room number for the reservation
LEVEL_NUMBER = 1 # Level number for the reservation
TITLE = "Physik Lerngruppe" # Title for the reservation
DESCRIPTION = "Erstes Zusammentreffen" # Description for the reservation
PERSONCOUNT = 6 # Person count for the reservation


def generate_link(date, start_time, end_time, room_number = 20, level_number = 1):
    # Generate a link for the reservation page with the given date and time
    formated_start_time = start_time.replace(':', '%3A')
    formated_end_time = end_time.replace(':', '%3A')
    base_url = "https://raumbuchung.slub-dresden.de/Web/reservation/"
    return f"{base_url}?rid={room_number}&sid={level_number}&rd={date}&sd={date}{formated_start_time}&ed={date}{formated_end_time}"

LINK = generate_link(DATE, START_TIME, END_TIME, ROOM_NUMBER, LEVEL_NUMBER) # Generate the link for the reservation page

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

TitleInput = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'reservation-title'))
) # Wait for the title input field to be present

DescriptionInput = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'reservation-description'))
) # Wait for the description input field to be present

PersonCountInput = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'react-select-2-input'))
) # Wait for the person count input field to be present

ReservationTermsCheckbox = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'reservation-terms-checkbox'))
) # Wait for the privacy checkbox to be present

SubmitButton2 = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'btn-primary'))
) # Wait for the submit button to be present

TitleInput.send_keys(TITLE) # Enter the title
DescriptionInput.send_keys(DESCRIPTION) # Enter the description
PersonCountInput.send_keys(f"{PERSONCOUNT}" + Keys.ENTER) # Enter the person count
ReservationTermsCheckbox.click() # Click the privacy checkbox
SubmitButton2.click() # Click the submit button

# Wait for 10 seconds
time.sleep(10)



# Close the browser
driver.quit()