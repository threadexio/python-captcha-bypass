from selenium import webdriver
from time import sleep
import selenium

from captcha_bypass import solve_captcha

# Selenium browser setup
options = webdriver.ChromeOptions()


# Headless?
#options.add_argument("--headless")

options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

browser = webdriver.Chrome(options=options)

browser.get("https://www.google.com/recaptcha/api2/demo")

sleep(1)

# Filter through all the iframes on the page and find the one that corresponds to the captcha
iframes = browser.find_elements_by_tag_name("iframe")
for iframe in iframes:
	if iframe.get_attribute("src").startswith("https://www.google.com/recaptcha/api2/anchor"):
		captcha = iframe

result = solve_captcha(browser, captcha)

print(result)
# Travis CI stuff
if result:
	exit(0)
else:
	exit(1)