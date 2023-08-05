from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time 
import re
import os

SearchName =""
usernameIds=""
passwordIds=""
scroll_Value=5

def removeFile(fileNameDelete):
    file_path = fileNameDelete

    # Check if the file exists before attempting to delete it
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} deleted successfully.")
    else:
        print(f"{file_path} does not exist.")

def extectMailID():
    # Read the text document
    with open("page_source.html", "r", encoding="utf-8") as file:
        text = file.read()

    # Define a regex pattern to match email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(?!png)[A-Z|a-z]{2,7}\b'

    # Find all email addresses in the text using the regex pattern
    new_emails = re.findall(email_pattern, text)

    # Read existing emails from the existing email text file (if it exists)
    existing_emails = set()
    try:
        with open("email_list.txt", "r", encoding="utf-8") as email_file:
            existing_emails.update(line.strip() for line in email_file)
    except FileNotFoundError:
        pass

    # Add new emails to the existing set and write them back to the text file
    with open("email_list.txt", "a", encoding="utf-8") as email_file:
        for email in new_emails:
            if email not in existing_emails:
                existing_emails.add(email)
                email_file.write(email + "\n")

    # Print the extracted email addresses
    for email in existing_emails:
        print(email)
    existing_emails = set()
    try:
        with open("email_list.txt", "r", encoding="utf-8") as email_file:
            existing_emails.update(line.strip() for line in email_file)
    except FileNotFoundError:
        pass

    # Write unique email addresses back to the text file
    with open("email_list.txt", "w", encoding="utf-8") as email_file:
        for email in existing_emails:
            email_file.write(email + "\n")


try:
    removeFile("page_source.html")
except:
    print(None)

driver = webdriver.Chrome(r'chrome-win64')  # Optional argument, if not specified will search path.

driver.get('https://www.linkedin.com/login');

input_box = driver.find_element(By.ID, "username")  # Replace with appropriate locator
input_box.send_keys(usernameIds)

input_box = driver.find_element(By.ID, "password")  # Replace with appropriate locator
input_box.send_keys(passwordIds)

element = driver.find_element(By.CLASS_NAME, "login__form_action_container ")
element.click()

driver.get('https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords='+SearchName+'&origin=FACETED_SEARCH&sid=T(l&sortBy=%22relevance%22');

for i in range(scroll_Value):
    time.sleep(10)
    scroll_amount = 50000  # Adjust this value as needed
    driver.execute_script(f"window.scrollBy(0, {scroll_amount});")

page_html = driver.page_source
with open("page_source.html", "w", encoding="utf-8") as file:
    file.write(page_html)

extectMailID()
