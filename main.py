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
from datetime import datetime, timedelta

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
    LINK = generate_link(date=date, start_time=start_time, end_time=end_time, room_number=room_number)  # Generate the link for the reservation page

    # Setup Chrome options and service
    service = Service(executable_path='/usr/bin/chromedriver')
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

    print(LINK)
    print(USERNAME)
    print(PASSWORD)
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
    #make a screenshot
    driver.save_screenshot('befor click.png')  # Save a screenshot of the page
    SubmitButton.click()  # Click the submit button
    time.sleep(2)  # Wait for the page to load
    driver.save_screenshot('after click.png')  # Save a screenshot of the page
    driver.get(LINK)  # Open the reservation page
    time.sleep(2)  # Wait for the page to load
    with open('page_source.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    
    if False:
        # Check Checkbox
        Checkbox3 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'accept'))
        )  # Wait for the checkbox to be present
        SubmitButton3 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'slubbutton'))
        )  # Wait for the submit button to be present
        
        Checkbox3.click()  # Click the checkbox
        driver.save_screenshot('befor click 2.png')  # Save a screenshot of the page
        SubmitButton3.click()  # Click the submit button
        time.sleep(5)  # Wait for the page to load
        driver.save_screenshot('after click 2.png')  # Save a screenshot of the page

        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll to the bottom of the page
        driver.save_screenshot('after click 3.png')  # Save a screenshot of the page
    if False:
        Checkbox3 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, '_shib_idp_rememberConsent'))
        )  # Wait for the checkbox to be present
        SubmitButton3 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="_eventId_proceed"]'))
        )  # Wait for the submit button to be present
        
        Checkbox3.click()  # Click the checkbox
        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll to the bottom of the page
        driver.save_screenshot('befor click 2.png')  # Save a screenshot of the page
        SubmitButton3.click()  # Click the submit button
        time.sleep(5)  # Wait for the page to load
        driver.save_screenshot('after click 2.png')  # Save a screenshot of the page


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
    driver.execute_script("arguments[0].scrollIntoView(true);", ReservationTermsCheckbox)
    time.sleep(10)  # Wait for the checkbox to be in view
    ReservationTermsCheckbox.click()  # Click the privacy checkbox
    SubmitButton2.click()  # Click the submit button

    # Wait for ... seconds
    time.sleep(pause)
    sucess = True if driver.find_elements(By.CLASS_NAME, 'success') else False  # Check if the reservation was successful
    # Close the browser
    driver.quit()
    return sucess  # Return the success status
    
def reserve_room(reservation, row_index, DATE:str, START_TIME:str, END_TIME:str, ROOM_NUMBERS:str, TITLE="Physik Lerngruppe", DESCRIPTION="Hausaufgaben", PERSON_COUNT=3):
    for ROOM_NUMBER in ROOM_NUMBERS:
        success = make_reservation(date=DATE, start_time=START_TIME, end_time=END_TIME, room_number=ROOM_NUMBER, title=TITLE, description=DESCRIPTION, person_count=PERSON_COUNT)
        if success:
            reservation["status"] = f"Success - Reservation for Room {ROOM_NUMBER}"
            print(f"Successfully made reservation for reservation {row_index} for Room {ROOM_NUMBER}")
            break
    if not success:
        reservation["status"] = "Failed for all Rooms"
        print(f"Failed to make reservation for reservation {row_index} for all rooms")

def run_reservation_script():
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

        if STATUS in ["Success - Reservation for Room 0.40", "Success - Reservation for Room 0.42", "Success - Reservation for Room 0.43", "Success - Reservation for Room 0.46", "Success - Reservation for Room 0.47", "Success - Reservation for Room 0.66", "Failed for all Rooms", "Skipped (Past)", "Skipped (Future)"]:
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

run_reservation_script()  # Run the script once at startup

# Schedule the script to run at every full hour
schedule.every().hour.at(":00").do(run_reservation_script)

print("Scheduler is running. Press Ctrl+C to stop.")

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)