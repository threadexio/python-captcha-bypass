#
# Python Captcha Bypass
# https://github.com/threadexio/python-captcha-bypass
#
#	MIT License
#

from pydub import AudioSegment
import speech_recognition as sr
import tempfile
import requests
import time
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import selenium


def solve_captcha(driver: selenium.webdriver, iframe, t=5) -> bool:
    """
    Solve the given captcha

    :Usage:
        result = solve_captcha(webdriver, captcha_iframe)

    :rtype: bool
    """

    tmp_dir = tempfile.gettempdir()
    mp3_file = os.path.join(tmp_dir, "_tmp.mp3")
    wav_file = os.path.join(tmp_dir, "_tmp.wav")

    # Switch current context
    driver.switch_to.frame(iframe)

    # Click the checkbox
    wait_for_elem(driver, By.CLASS_NAME, "recaptcha-checkbox-border", t).click()

    # Switch back to the main page
    # cause the actual captcha window
    # is on another iframe
    driver.switch_to.default_content()

    try:
        driver.switch_to.frame(wait_for_elem(
            driver, By.XPATH, '//iframe[@title="recaptcha challenge"]', t))

        # Get the audio challenge instead
        wait_for_elem(driver, By.ID, "recaptcha-audio-button", t).click()

        # Download & convert the file
        with open(mp3_file, "wb") as f:
            link = wait_for_elem(driver, By.CLASS_NAME, "rc-audiochallenge-tdownload-link", t).get_attribute("href")
            r = requests.get(link, allow_redirects=True)
            f.write(r.content)
            f.close()

        # Convert to wav here
        AudioSegment.from_mp3(mp3_file).export(wav_file, format="wav")

        # Using google's own api against them
        recognizer = sr.Recognizer()

        with sr.AudioFile(wav_file) as source:
            recorded_audio = recognizer.listen(source)
            text = recognizer.recognize_google(recorded_audio)

        # Type out the answer
        wait_for_elem(driver, By.ID, "audio-response", t).send_keys(text)

        # Click the "Verify" button to complete
        wait_for_elem(driver, By.ID, "recaptcha-verify-button", t).click()

        __cleanup([mp3_file, wav_file])

        # Return the text used for the answer
        return text

    except Exception as e:
        # If we encounter the "Your computer is sending automated requests..."
        # or something that doesn't allow the code to continue return false
        __cleanup([mp3_file, wav_file])
        print(e)
        return False


def __cleanup(files: list):
    for x in files:
        if os.path.exists(x):
            os.remove(x)


def wait_for_elem(driver: selenium.webdriver, locator_type: str, locator: str, timeout: int):
    """
    Simple wrapper around selenium's find_element -- added a simple mechanism to wait until the element we want is present
    """
    try:
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((locator_type, locator)))
    except TimeoutException:
        return False
