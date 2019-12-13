from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime as dt
import sys
import getpass
import re

def start_registration(handle, email, pwd1, pwd2):
    print("Starting registration, browser opening shortly...\n")
    driver = webdriver.Chrome()
    URL_TO_CONNECT = "https://codeforces.com/register"
    driver.get(URL_TO_CONNECT)

    handle_input = driver.find_element_by_name("handle")
    email_input = driver.find_element_by_name("email")
    pwd1_input = driver.find_element_by_name("password")
    pwd2_input = driver.find_element_by_name("passwordConfirmation")

    handle_input.send_keys(handle)
    email_input.send_keys(email)
    pwd1_input.send_keys(pwd1)
    pwd2_input.send_keys(pwd2)

    form = driver.find_element_by_id("registerForm")
    form.submit()

    try:
        # wait for next page to load
        WebDriverWait(driver, 10).until(EC.url_changes(URL_TO_CONNECT))

        current_datetime = dt.datetime.now()
        driver.save_screenshot(f"{current_datetime}.png")

        driver.close()
        print(f"Screenshot captured! Saved as {current_datetime}.png")
        print("Exiting...")
        sys.exit(1)
    except Exception:
        print("Session Timeout. Handle might already be taken.")
        print("Exiting...")

        driver.close()
        sys.exit(1)


def main():
    print('''
    _________            .___    ___________                          __________              .__          __                 __  .__                
\_   ___ \  ____   __| _/____\_   _____/__________   ____  ____   \______   \ ____   ____ |__| _______/  |_____________ _/  |_|__| ____   ____   
/    \  \/ /  _ \ / __ |/ __ \|    __)/  _ \_  __ \_/ ___\/ __ \   |       _// __ \ / ___\|  |/  ___/\   __\_  __ \__  \\   __\  |/  _ \ /    \  
\     \___(  <_> ) /_/ \  ___/|     \(  <_> )  | \/\  \__\  ___/   |    |   \  ___// /_/  >  |\___ \  |  |  |  | \// __ \|  | |  (  <_> )   |  \ 
 \______  /\____/\____ |\___  >___  / \____/|__|    \___  >___  >  |____|_  /\___  >___  /|__/____  > |__|  |__|  (____  /__| |__|\____/|___|  / 
        \/            \/    \/    \/                    \/    \/          \/     \/_____/         \/                   \/                    \/  
    ''')
    handle = input("Enter your username/handle to use: ")

    while True:
        email = input("Enter your email to use: ")
        if re.match('.+@{1}.+[.]{1}.+', email):
            break
        else:
            print("Please enter a valid email.\n")

    while True:
        pwd1 = getpass.getpass(prompt="Enter password: ")
        pwd2 = getpass.getpass(prompt="Enter password again: ")

        if pwd1 != pwd2:
            print("Passwords don't match.\n")
        elif not re.match("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#\$%\^&]).{5,}$", pwd1):
            # registration page checks for password strength
            print("Password must be >5 in length, have lowercase, uppercase, numbers and special characters.\n")
        else:
            break

    start_registration(handle, email, pwd1, pwd2)


if __name__ == '__main__':
    main()
