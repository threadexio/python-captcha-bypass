from selenium import webdriver
from time import sleep

import selenium
import re

import main

capabilities = webdriver.DesiredCapabilities.FIREFOX
capabilities["marionette"] = True

browser = webdriver.Firefox(firefox_binary="/usr/bin/firefox", executable_path="../files/geckodriver", capabilities=capabilities)

'''
browser.get("https://discord.com/")

browser.find_element_by_class_name("gtm-click-class-open-button").click()

sleep(1)

forms = browser.find_elements_by_tag_name("form")
divs = browser.find_elements_by_tag_name("div")

for form in forms:
	if re.match("form-([a-zA-Z0-9]{6})", form.get_attribute("class")):
		correct_form = form

for div in divs:
	if re.match("checkbox-([a-zA-Z0-9]{6})", div.get_attribute("class")):
		correct_div = div


correct_form.find_elements_by_tag_name("input")[0].send_keys("ghhuuuuuuuuuuptesrigbv")
correct_div.click()

sleep(0.5)

correct_form.find_elements_by_tag_name("button")[0].click()
'''


browser.get("https://www.google.com/recaptcha/api2/demo")

sleep(1)

iframes = browser.find_elements_by_tag_name("iframe")

for iframe in iframes:
	if iframe.get_attribute("src").startswith("https://www.google.com/recaptcha/api2/anchor"):
		captcha = iframe

main.solve_captcha(browser, captcha)