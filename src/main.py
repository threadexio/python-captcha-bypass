from selenium import webdriver
from time import sleep
import selenium

checkbox_class = "recaptcha-checkbox-border"

def solve_captcha(driver :webdriver.Firefox, iframe) -> bool:
	# Switch current context
	driver.switch_to.frame(iframe)

	# Get the checkbox
	checkbox = driver.find_elements_by_class_name(checkbox_class)[0]

	# Click the checkbox
	checkbox.click()

	sleep(1)

	driver.switch_to.default_content()

	sleep(1)

	iframes = driver.find_elements_by_tag_name("iframe")

	iframes = driver.find_elements_by_tag_name("iframe")
	for x in iframes:
		if x.get_attribute("title") == "recaptcha challenge":
			driver.switch_to.frame(x)

	sleep(1)

	driver.find_element_by_id("recaptcha-audio-button").click()