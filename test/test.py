from selenium import webdriver
from time import sleep

import selenium
import re

capabilities = webdriver.DesiredCapabilities.FIREFOX
capabilities["marionette"] = True

browser = webdriver.Firefox(firefox_binary="/usr/bin/firefox", executable_path="../files/geckodriver", capabilities=capabilities)

browser.get("https://discord.com/")

browser.find_element_by_class_name("gtm-click-class-open-button").click()

sleep(1)

browser.find_elements_by_tag_name("forms")

for form in forms:
	if (re)