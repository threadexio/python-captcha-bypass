import speech_recognition as sr
from pydub import AudioSegment
import requests
import time
import os

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

		# Find the correct iframe and switch to it
		iframes = driver.find_elements_by_tag_name("iframe")
		for x in iframes:
			if x.get_attribute("title") == "recaptcha challenge":
				driver.switch_to.frame(x)

		time.sleep(_pause)

		driver.find_element_by_id("recaptcha-audio-button").click()

		time.sleep(_pause)

		# Download & convert the file
		with open(mp3_file, "wb") as f:
			link = driver.find_element_by_class_name("rc-audiochallenge-tdownload-link").get_attribute("href")
			r = requests.get(link, allow_redirects=True)
			f.write(r.content)
			f.close()
			sound = AudioSegment.from_mp3(mp3_file)
			sound.export(wav_file, format="wav")

		# Using google's own api against them
		recognizer = sr.Recognizer()

		with sr.AudioFile(wav_file) as source:
			recorded_audio = recognizer.listen(source)
			text = recognizer.recognize_google(recorded_audio)

		# Type out the answer
		driver.find_element_by_id("audio-response").send_keys(text)

		# Click the "Verify" button to complete
		driver.find_element_by_id("recaptcha-verify-button").click()

		# Cleanup created files
		if os.path.exists(mp3_file):
			os.remove(mp3_file)
		if os.path.exists(wav_file):
			os.remove(wav_file)

		# Return the text used for the answer
		return text

	except Exception as e:
		# If we encounter the "Your computer is sending automated requests..."
		# or something that doesn't allow the code to continue return false

		# Cleanup created files
		if os.path.exists(mp3_file):
			os.remove(mp3_file)
		if os.path.exists(wav_file):
			os.remove(wav_file)

		return False
