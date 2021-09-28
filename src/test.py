from selenium import webdriver
from time import sleep
import selenium

import captcha_bypass

# Selenium browser setup
options = webdriver.ChromeOptions()


# Headless?
options.add_argument("--headless")

options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

browser = webdriver.Chrome(options=options)

browser.get("https://www.google.com/recaptcha/api2/demo")



# Filter through all the iframes on the page and find the one that corresponds to the captcha
iframes = browser.find_elements_by_tag_name("iframe")
for iframe in iframes:
    if iframe.get_attribute("src").startswith("https://www.google.com/recaptcha/api2/anchor"):
        captcha = iframe

result = captcha_bypass.solve_captcha(browser, captcha)

# do error checking here

"""
# are we ratelimited?
if result[0] == captcha_bypass.status.RATELIMITED:
    # do stuff here

# is the network or the server too slow?
elif result[0] == captcha_bypass.status.TIMEOUT
    # do stuff here

else:
"""

if result:
    print(result)
    exit(0)
else:
    print("Failed!")
    exit(1)
