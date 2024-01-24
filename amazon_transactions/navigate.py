"""This module contains functions to navigate to Amazon and login to the account"""
import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def save_cookies(driver: webdriver.Firefox):
    """Get and store cookies after login"""
    cookies = driver.get_cookies()

    # Store cookies in a file
    with open("cookies.json", "w", encoding="utf-8") as file:
        json.dump(cookies, file)
    print("New Cookies saved successfully")


def load_cookies(driver: webdriver.Firefox):
    """Load cookies from file and add to browser session"""
    # Check if cookies file exists
    if "cookies.json" in os.listdir():
        # Load cookies to a vaiable from a file
        with open("cookies.json", "r", encoding="utf-8") as file:
            cookies = json.load(file)

        # Set stored cookies to maintain the session
        for cookie in cookies:
            driver.add_cookie(cookie)
            
        print("Cookies loaded successfully")
    else:
        print("No cookies file found")

    driver.refresh()  # Refresh Browser after login


def login_to_amazon(driver: webdriver.Firefox, email: str, password: str):
    """Login to Amazon.com"""
    print("Logging in...")
    # Navigate to Amazon
    driver.get("https://www.amazon.com/")

    load_cookies(driver)

    # Find the sign-in link and click it
    driver.find_element(By.ID, "nav-link-accountList").click()

    # Wait for the page to load
    time.sleep(2)

    if "signin" in driver.current_url:
        # Find the email field, enter our email, and press Enter
        driver.find_element(By.ID, "ap_email").send_keys(email + Keys.RETURN)

        # Wait for the page to load
        time.sleep(2)

        # Find the password field, enter our password, and press Enter
        driver.find_element(By.ID, "ap_password").send_keys(password + Keys.RETURN)

        # Detect when user enters 2FA code
        input("Press Enter after you have entered your 2FA code")

        # Wait for the page to load
        time.sleep(2)

        save_cookies(driver)

        return driver

    else:
        return driver
