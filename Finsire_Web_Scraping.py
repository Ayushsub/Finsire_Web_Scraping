from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os
import sys

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage') 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def login(driver, username, password):
    driver.get('https://www.saucedemo.com/')
    username_field = driver.find_element(By.ID, 'user-name')
    password_field = driver.find_element(By.ID, 'password')
    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button = driver.find_element(By.ID, 'login-button')
    login_button.click()
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'inventory_list'))
        )
        print("Login successful")
        return True
    except:
        print("Login failed or CAPTCHA detected")
        driver.quit()
        return False

def scrape_data(driver):
    driver.get('https://www.saucedemo.com/inventory.html')
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'inventory_item'))
    )
    items = driver.find_elements(By.CLASS_NAME, 'inventory_item')
    data = []
    for item in items:
        name = item.find_element(By.CLASS_NAME, 'inventory_item_name').text
        price = item.find_element(By.CLASS_NAME, 'inventory_item_price').text
        data.append([name, price])
    with open('scraped_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Item Name', 'Price'])
        writer.writerows(data)
    print("Data scraping completed and saved to scraped_data.csv")

def get_credentials():
    """Prompts the user for their username and password."""
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    return username, password

if __name__ == "__main__":
    username, password = get_credentials()
    print("Logging in...")

    driver = setup_driver()
    if not login(driver, username, password):
        sys.exit(1)

    scrape_data(driver)
    driver.quit()
