#
# Python Captcha Bypass
# https://github.com/threadexio/python-captcha-bypass
#
# GNU General Public License v3.0
#

import speech_recognition as sr
import subprocess
import requests
import time
import os

# driver: webdriver
# iframe: Captcha iframe
# _pause: Secs to wait between each click

def solve_captcha(driver, iframe, _pause = 2) -> bool:
	mp3_file = "_tmp.mp3"
	wav_file = "_tmp.wav"

	# Switch current context
	driver.switch_to.frame(iframe)

	# Get the checkbox
	checkbox = driver.find_element_by_class_name("recaptcha-checkbox-border")

	# Click the checkbox
	checkbox.click()

	time.sleep(_pause)

	# Switch back to the main page
	# cause the actual captcha window
	# is on another iframe
	driver.switch_to.default_content()

	try:
		driver.switch_to.frame( driver.find_element_by_xpath('//iframe[@title="recaptcha challenge"]') )

		driver.find_element_by_id("recaptcha-audio-button").click()

		time.sleep(_pause)

		# Download & convert the file
		with open(mp3_file, "wb") as f:
			link = driver.find_element_by_class_name("rc-audiochallenge-tdownload-link").get_attribute("href")
			r = requests.get(link, allow_redirects=True)
			f.write(r.content)
			f.close()

		# Just call ffmpeg directly instead of using pydub
		# Also set stdin, stdout, stderr to /dev/null or nul
		with open(os.devnull, "w") as f:
			subprocess.Popen(["ffmpeg", "-i", mp3_file, wav_file], stdin=f, stdout=f, stderr=f).communicate()

		# Using google's own api against them
		recognizer = sr.Recognizer()

		with sr.AudioFile(wav_file) as source:
			recorded_audio = recognizer.listen(source)
			text = recognizer.recognize_google(recorded_audio)

		# Type out the answer
		driver.find_element_by_id("audio-response").send_keys(text)

		# Click the "Verify" button to complete
		driver.find_element_by_id("recaptcha-verify-button").click()

		__cleanup([ mp3_file, wav_file ])

		# Return the text used for the answer
		return text

	except Exception as e:
		# If we encounter the "Your computer is sending automated requests..."
		# or something that doesn't allow the code to continue return false
		__cleanup([ mp3_file, wav_file ])
		print(e)
		return False

def __cleanup(files):
	for x in files:
		if os.path.exists(x):
			os.remove(x)
