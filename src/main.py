import selenium

checkbox_class = "recaptcha-checkbox-border"

def solve_captcha(driver, iframe) -> bool:
	# Switch current context
	driver.switch_to.frame(iframe)

	# Get the checkbox
	checkbox = driver.find_elements_by_class_name(checkbox)

	print(checkbox)
