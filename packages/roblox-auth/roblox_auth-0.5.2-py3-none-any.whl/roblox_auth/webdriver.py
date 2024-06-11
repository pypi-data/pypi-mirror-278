
import time
import os

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

roblox_url = "https://www.roblox.com/newlogin"

def status(text):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[1;34m" + text + "\033[0m")

def get_cookie(File: bool = False):
    """
    Opens the Roblox login page using Selenium.
    
    """
    try:
        status("Starting to create an account...")
        cookie_found = False
        elapsed_time = 0
        time.sleep(.3)
        
        status("Initializing webdriver...")
        driver = webdriver.Chrome()
        driver.set_window_size(1200, 800)
        driver.set_window_position(0, 0)
        driver.get(roblox_url)
        time.sleep(2)
    
        status("searching for items on the website")
        try:
            accept_all_button = driver.find_element(By.CSS_SELECTOR, ".cookie-btn-float .btn-cta-lg")
            status("Accepting cookies...")
            accept_all_button.click()
            time.sleep(0.3)
        except Exception:
            status("Confirming...")
        
        while not cookie_found and elapsed_time < 180:
            status("Waiting for the cookie...")
            time.sleep(3)
            elapsed_time += 3
            for cookie in driver.get_cookies():
                if cookie.get('name') == '.ROBLOSECURITY':
                    cookie_found = True
                    break
        
        if File: file_name = "Cookies.txt"; file_path = os.path.abspath(file_name)
        
        if cookie_found:
            status("Cookie found...")
            if File:
                with open(file_name, "a") as file:
                    file.write(f"\n\n{cookie.get('value')}\n\n")
                status(f"Cookie has been saved to {file_path}")
            return cookie.get('value')
        
        return None
    
    except Exception as e:
        raise e
    
