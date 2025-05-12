#import Selenium Libaries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Import the other libraries
import time
import schedule
import json
import os
import sys
from datetime import datetime, timedelta

SYSTEM_IS_WINDOWS = True  # Set to True if running on Windows
CHROMEDRIVER_PATH = './chromedriver.exe' if SYSTEM_IS_WINDOWS else '/usr/bin/chromedriver' # Path to your chromedriver executable

# Load data from JSON file
json_path = os.path.join(os.path.dirname(__file__), 'data.json')
with open(json_path, 'r') as json_file:
    reservations = json.load(json_file)

def generate_link(date:str, start_time:str, end_time:str, room_number="0.66"):
    # Generate a link for the reservation page with the given date and time
    formated_start_time = start_time.replace(':', '%3A')
    formated_end_time = end_time.replace(':', '%3A')
    base_url = "https://raumbuchung.slub-dresden.de/Web/reservation/"
    formated_room_number = 18 if room_number == "0.40" else 19 if room_number == "0.42" else 20 if room_number == "0.43" else 21 if room_number == "0.46" else 22 if room_number == "0.47" else 23
    level_number = 1
    return f"{base_url}?rid={formated_room_number}&sid={level_number}&rd={date}&sd={date}{formated_start_time}&ed={date}{formated_end_time}"

def make_reservation(date:str, start_time:str, end_time:str, room_number=20, title="Physik Lerngruppe", description="Hausaufgaben", person_count=1, pause=1):
    
    print("Generating link...")
    LINK = generate_link(date=date, start_time=start_time, end_time=end_time, room_number=room_number)  # Generate the link for the reservation page
    # Setup Chrome options and service
    service = Service(executable_path=CHROMEDRIVER_PATH)
    #service = Service(executable_path='chromedriver.exe')  # Path to your chromedriver executable
    options = webdriver.ChromeOptions()
    #options.add_argument('-headless')  # Run in headless mode (no GUI)
    driver = webdriver.Chrome(service=service, options=options)  # Initialize the WebDriver
    # Load credentials from config file using a relative path
    config_path = os.path.join(os.path.dirname(__file__), './config.json')
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    USERNAME = config['username']
    PASSWORD = config['password']

    print("Logging in...")
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
    driver.execute_script("arguments[0].scrollIntoView(true);", SubmitButton)  # Scroll to the submit button
    time.sleep(2)  # Wait for the button to be in view
    SubmitButton.click()  # Click the submit button
    time.sleep(2)  # Wait for the page to load
    
    print("Checking for first interrupt...")
    try:
        # Check Checkbox
        Checkbox3 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'accept'))
        )  # Wait for the checkbox to be present
        SubmitButton3 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'slubbutton'))
        )  # Wait for the submit button to be present
        
        Checkbox3.click()  # Click the checkbox
        SubmitButton3.click()  # Click the submit button
        print("First interrupt found and handled")
    except:
        print("First interrupt not found, Proceeding without it")
    
    print("Checking for second interrupt...")
    try:
        Checkbox3 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, '_shib_idp_rememberConsent'))
        )  # Wait for the checkbox to be present
        SubmitButton3 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="_eventId_proceed"]'))
        )  # Wait for the submit button to be present
        
        Checkbox3.click()  # Click the checkbox
        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll to the bottom of the page
        SubmitButton3.click()  # Click the submit button
        print("Second interrupt found and handled")
    except:
        print("Second interrupt not found, Proceeding without it")
    
    print("Continuing with reservation...")
    driver.get(LINK)  # Open the reservation page
    time.sleep(2)  # Wait for the page to load

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
    
    
    print("Found all elements, filling out the form...")
    TitleInput.send_keys(title)  # Enter the title
    DescriptionInput.send_keys(description)  # Enter the description
    PersonCountInput.send_keys(f"{person_count}" + Keys.ENTER)  # Enter the person count
    driver.execute_script("arguments[0].scrollIntoView(true);", ReservationTermsCheckbox)
    print("Waiting for checkbox to be in view...")
    time.sleep(2)  # Wait for the checkbox to be in view
    print("Submitting the form...")
    ReservationTermsCheckbox.click()  # Click the privacy checkbox
    SubmitButton2.click()  # Click the submit button

    # Wait for ... seconds
    time.sleep(pause)
    sucess = True if driver.find_elements(By.CLASS_NAME, 'success') else False  # Check if the reservation was successful
    # Close the browser
    print("Reservation was successful" if sucess else "Reservation failed")
    driver.quit()
    print("Browser closed")
    return sucess  # Return the success status
    
def reserve_room(reservation, row_index, DATE:str, START_TIME:str, END_TIME:str, ROOM_NUMBERS:str, TITLE="Physik Lerngruppe", DESCRIPTION="Hausaufgaben", PERSON_COUNT=3, REPEAT="no"):
    for ROOM_NUMBER in ROOM_NUMBERS:
        success = make_reservation(date=DATE, start_time=START_TIME, end_time=END_TIME, room_number=ROOM_NUMBER, title=TITLE, description=DESCRIPTION, person_count=PERSON_COUNT)
        if success:
            if REPEAT == "no":
                reservation["status"] = f"Success"
            else:
                reservation["status"] = f"Success - Reserved until {DATE}"
            print(f"Successfully made reservation {row_index} for Room {ROOM_NUMBER} on {DATE} from {START_TIME} to {END_TIME}")
            break
    if not success:
        reservation["status"] = "Failed for all Rooms"
        print(f"Failed to make reservation for reservation {row_index} for all rooms")

def run_reservation_script():
    old_stdout = sys.stdout
    log_file = open(f"log/{datetime.now().strftime('%m-%d-%Y_%H-%M-%S')}.log","w")
    sys.stdout = log_file

    for row_index, reservation in enumerate(reservations):
        DATE = reservation["date"]
        START_TIME = reservation["start_time"]
        END_TIME = reservation["end_time"]
        ROOM_NUMBERS = reservation["room_numbers"]
        TITLE = reservation["title"]
        DESCRIPTION = reservation["description"]
        PERSON_COUNT = reservation["person_count"]
        STATUS = reservation["status"]
        REPEAT = reservation["repeat"]
        current_date = datetime.now().date()
        formated_date = datetime.strptime(DATE, '%Y-%m-%d').date()
        print(f"Processing reservation {row_index} with status: {STATUS}...")

        if STATUS in ["Success", "Failed for all Rooms", "Skipped (Past)", "Skipped (Future)"]:
            print(f"Skipping reservation {row_index} with status: {STATUS}")
            continue

        if (formated_date - current_date).days < 0:
            if REPEAT == "no":
                reservation["status"] = "Skipped (Past)"
                print(f"Skipping reservation {row_index} with status: Skipped (Past)")
                continue
            else:
                while (formated_date - current_date).days < 0:
                    formated_date = formated_date + + timedelta(days=7) if REPEAT == "weekly" else formated_date + timedelta(days=14) if REPEAT == "biweekly" else formated_date
                reserve_room(reservation, row_index, formated_date.strftime('%Y-%m-%d'), START_TIME, END_TIME, ROOM_NUMBERS, TITLE, DESCRIPTION, PERSON_COUNT)
                formated_date = formated_date + timedelta(days=7) if REPEAT == "weekly" else formated_date + timedelta(days=14) if REPEAT == "biweekly" else formated_date

        if (formated_date - current_date).days > 14:
            reservation["status"] = "Skipped (Future)"
            print(f"Skipping reservation {row_index} with status: Skipped (Future)")
            continue

        reserve_room(reservation, row_index, formated_date.strftime('%Y-%m-%d'), START_TIME, END_TIME, ROOM_NUMBERS, TITLE, DESCRIPTION, PERSON_COUNT)



    # Save updated statuses back to the JSON file
    with open(json_path, 'w') as json_file:
        json.dump(reservations, json_file, indent=4)
    print("Reservations completed. JSON file updated.")
    sys.stdout = old_stdout
    log_file.close()

print("Starting reservation script...")
run_reservation_script()  # Run the script once at startup

# Schedule the script to run at every full hour
schedule.every().hour.at(":00").do(run_reservation_script)

print("Scheduler is running. Press Ctrl+C to stop.")

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)