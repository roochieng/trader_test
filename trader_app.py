from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
from plyer import notification


load_dotenv()


today_date = datetime.today().strftime('%Y-%m-%d')
url = os.environ.get('URL')

# Set the path to your ChromeDriver executable
chrome_driver_path = "C:/Users/Me/Desktop/Test/chromedriver-win64/chromedriver.exe"

# Create Chrome options
chrome_options = Options()

# Open chrome in background mode
# chrome_options.add_argument("--headless")

# Create a Chrome webdriver with options
service = ChromeService(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the URL in the browser
driver.get(url)


# Get logins

login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'btn__login')))
login_button.click()

username_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'txtEmail')))

password_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'txtPass')))
submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"].button.secondary')))

# Enter login credentials
username_input.send_keys(os.environ.get('_USERNAME'))
password_input.send_keys(os.environ.get('PASSWORD'))

# Submit the form
submit_button.click()
time.sleep(5)

# file and data storage
new_file = 'data.txt'
last_digit = []
last_two_values = [0, 1]

count = 0
while count < 100:
    if last_two_values[0] != last_two_values[1]:
        spot_span = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'spot')))

        trade_value = spot_span.get_attribute('data-value')
        last_two_values.insert(0, trade_value)
        decimal_part = abs(float(trade_value)) % 1
        decimal_part = round(decimal_part, 3)
        fractional_str = str(decimal_part)
        decimal_digits = fractional_str.split('.')[1]
        print(trade_value)
        try:
            second_digit = decimal_digits[1]
        except IndexError:
            second_digit = 0
        print(second_digit)
        last_digit.insert(0, second_digit)
        with open(new_file, 'a') as file:
            file.write(f'{second_digit}\n')
        if len(last_digit) > 2:
            last_digit.pop()
        if len(last_two_values) > 2:
            last_two_values.pop()
    else:
        pass
    count += 1
    time.sleep(1)

print(last_digit)
print(last_two_values)
time.sleep(10)

# Close the browser window
driver.quit()