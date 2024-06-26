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
chrome_driver_path = "/home/me/Dependancies/chromedriver-linux64/chromedriver"

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

# Click on demo
account_switch = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "acc_switcher")))
account_switch.click()
time.sleep(1)
demo_switch = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Demo")))
demo_switch.click()

demo = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div[data-value="VRTC10415542"]')))
demo.click()
time.sleep(5)


# Get Account balance
def get_account_balance():
    balance_div = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'header__acc-balance')))
    balance_text = balance_div.text
    balance_value = balance_text.split()[0]
    balance_value = balance_value.replace(',', '')
    balance_value = float(balance_value)
    return balance_value


# Update stake
def update_stake(balance):
    amount_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'amount')))
    amount_input.clear()
    new_text = int(balance) // 10
    amount_input.send_keys(new_text)

update_stake(get_account_balance())
time.sleep(5)


# Click buy
def purchase():
    locator = (By.ID, 'purchase_button_top')
    purchase = button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locator))
    purchase.click()


def close_bet_window():
    locator = (By.ID, 'close_confirmation_container')
    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locator))
        element.click()
    except Exception as e:
        print(f"Failed to click the element: {str(e)}")

# file and data storage
new_file = f"app_demo_data_{today_date}.txt"
last_digit = [3, 10, 20]
last_two_values = [0, 1]

loses = 0
wins = 0
count = 0
while count < 50000:
    spot_span = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'spot')))
    trade_value = spot_span.get_attribute('data-value')
    if trade_value != last_two_values[0]:
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
            file.write(f'trade value: {last_two_values[0]}, last digit: {second_digit}\n')
        if int(last_digit[0]) < 2 and int(last_digit[1]) < 2:
            purchase()
            close_bet_window()
            with open(new_file, 'a') as file:
                file.write(f'purchased: {last_digit}\n')
        if len(last_digit) > 6:
            last_digit.pop()
        if len(last_two_values) > 2:
            last_two_values.pop()
        if int(last_digit[0]) < 2 and int(last_digit[1]) < 2 and int(last_digit[2]) < 2:
            loses += 1
            print(f"Number of loses: {loses}")
            with open(new_file, 'a') as file:
                file.write(f"Number of loses: {loses}\n")
        elif int(last_digit[0]) > 2 and int(last_digit[1]) < 2 and int(last_digit[2]) < 2:
            wins  += 1
            print(f"Number of wins: {wins}")
            with open(new_file, 'a') as file:
                file.write(f"Number of wins: {wins}\n")
        try:
            if loses > 0 and wins == 0:
                continue
            if (wins > 3 and loses == 0) or wins // loses <= 3:
                break
        except ZeroDivisionError:
            continue
        count += 1

time.sleep(10)

# Close the browser window
driver.quit()