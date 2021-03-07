from selenium import webdriver
from time import sleep
import selenium

from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox

from captcha_bypass import solve_captcha

# Selenium browser setup
capabilities = webdriver.DesiredCapabilities.FIREFOX
capabilities["marionette"] = True
options = Options()

# Headless?
#options.add_argument("--headless")

browser = webdriver.Firefox(executable_path="../files/geckodriver", capabilities=capabilities, options=options)

browser.get("https://www.google.com/recaptcha/api2/demo")

sleep(1)

# Filter through all the iframes on the page and find the one that corresponds to the captcha
iframes = browser.find_elements_by_tag_name("iframe")
for iframe in iframes:
	if iframe.get_attribute("src").startswith("https://www.google.com/recaptcha/api2/anchor"):
		captcha = iframe

print(solve_captcha(browser, captcha))