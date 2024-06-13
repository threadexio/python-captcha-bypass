from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep

import captcha_bypass  # Import your captcha bypass module here

# Selenium browser configuration
options = Options()

# Set browser language
options.add_experimental_option('prefs', {'intl.accept_languages': 'en'})

# Additional options, if needed
# options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# WebDriver initialization
try:
    browser = webdriver.Chrome(options=options)
except Exception as e:
    print(f"Error initializing WebDriver: {e}")
    exit(1)

try:
    browser.get("https://www.google.com/recaptcha/api2/demo")
    sleep(2)  # Wait for page to load
except Exception as e:
    print(f"Error navigating to page: {e}")
    browser.quit()
    exit(1)

# Find the captcha iframe
try:
    captcha = None
    iframes = browser.find_elements(By.TAG_NAME, "iframe")
    for iframe in iframes:
        if iframe.get_attribute("src").startswith("https://www.google.com/recaptcha/api2/anchor"):
            captcha = iframe
            break
    if not captcha:
        raise Exception("Captcha iframe not found")
except Exception as e:
    print(f"Error finding captcha iframe: {e}")
    browser.quit()
    exit(1)

# Solve the captcha
try:
    result = captcha_bypass.solve_captcha(browser, captcha)
    # Assuming solve_captcha returns a valid result
except Exception as e:
    print(f"Error solving captcha: {e}")
    browser.quit()
    exit(1)

# Check the result and handle accordingly
if result:
    print(result)
    exit(0)
else:
    print("Failed to solve the captcha!")
    exit(1)
