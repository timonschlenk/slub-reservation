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
from openpyxl import load_workbook  # Import openpyxl to read Excel files
from datetime import datetime

# Load data from Excel file
excel_path = os.path.join(os.path.dirname(__file__), 'data.xlsx')
workbook = load_workbook(excel_path)
sheet = workbook.active

def generate_link(date:str, start_time:str, end_time:str, room_number=20, level_number=1):
    # Generate a link for the reservation page with the given date and time
    formated_start_time = start_time.replace(':', '%3A')
    formated_end_time = end_time.replace(':', '%3A')
    base_url = "https://raumbuchung.slub-dresden.de/Web/reservation/"
    return f"{base_url}?rid={room_number}&sid={level_number}&rd={date}&sd={date}{formated_start_time}&ed={date}{formated_end_time}"

def make_reservation(date:str, start_time:str, end_time:str, room_number=20, level_number=1, title="Physik Lerngruppe", description="Hausaufgaben", person_count=1):
    LINK = generate_link(date=date, start_time=start_time, end_time=end_time, room_number=room_number, level_number=level_number)  # Generate the link for the reservation page

    # Setup Chrome options and service
    service = Service(executable_path='./chromedriver.exe')
    driver = webdriver.Chrome(service=service)

    # Load credentials from config file using a relative path
    config_path = os.path.join(os.path.dirname(__file__), './config.json')
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)

    USERNAME = config['username']
    PASSWORD = config['password']

    # Execute the script
    driver.get(LINK)  # Open the reservation page
    SubmitButton = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'btn-large'))
    )  # Wait for the submit button to be clickable
    SubmitButton.click()  # Click the submit button

    UsernameInput = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'txtUsername'))
    )  # Wait for the username input field to be present

    PasswordInput = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'txtPassword'))
    )  # Wait for the password input field to be present 

    SubmitButton = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'btnLogin'))
    )  # Wait for the submit button to be present

    UsernameInput.send_keys(USERNAME)  # Enter the username
    PasswordInput.send_keys(PASSWORD)  # Enter the password
    SubmitButton.click()  # Click the submit button

    TitleInput = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'reservation-title'))
    )  # Wait for the title input field to be present

    DescriptionInput = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'reservation-description'))
    )  # Wait for the description input field to be present

    PersonCountInput = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'react-select-2-input'))
    )  # Wait for the person count input field to be present

    ReservationTermsCheckbox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'reservation-terms-checkbox'))
    )  # Wait for the privacy checkbox to be present

    SubmitButton2 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'btn-primary'))
    )  # Wait for the submit button to be present

    TitleInput.send_keys(title)  # Enter the title
    DescriptionInput.send_keys(description)  # Enter the description
    PersonCountInput.send_keys(f"{person_count}" + Keys.ENTER)  # Enter the person count
    ReservationTermsCheckbox.click()  # Click the privacy checkbox
    SubmitButton2.click()  # Click the submit button

    # Wait for 3 seconds
    time.sleep(3)

    # Close the browser
    driver.quit()

for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, min_col=1, max_col=8, values_only=True):
    DATE = row[0]               # Column A: Date
    START_TIME = row[1]         # Column B: Start Time
    END_TIME = row[2]           # Column C: End Time
    ROOM_NUMBER = row[3]        # Column D: Room Number
    LEVEL_NUMBER = row[4]       # Column E: Level Number
    TITLE = row[5]              # Column F: Title
    DESCRIPTION = row[6]        # Column G: Description
    PERSON_COUNT = row[7]       # Column H: Person Count
    current_date = datetime.now().date()  # Get the current date
    formated_date = datetime.strptime(DATE, '%Y-%m-%d').date()
    
    if (formated_date - current_date).days < 0:
        print(f"Skipping reservation for {DATE} as it is in the past.")
        continue
    if (formated_date - current_date).days > 14:
        print(f"Skipping reservation for {DATE} as it is more than 14 days in the future.")
        continue
    make_reservation(date=DATE, start_time=START_TIME, end_time=END_TIME, room_number=ROOM_NUMBER, level_number=LEVEL_NUMBER, title=TITLE, description=DESCRIPTION, person_count=PERSON_COUNT)  # Call the function to make the reservation
