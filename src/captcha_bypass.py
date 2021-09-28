#
# Python Captcha Bypass
# https://github.com/threadexio/python-captcha-bypass
#
#	MIT License
#

from enum import Enum
from typing import Tuple
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


class status(Enum):
    SUCCESS = 0
    UNKNOWN = 1
    RATELIMITED = 2
    TIMEOUT = 3


class NotExistent(Exception):
    """
    This exception is used internally
    """
    err = None

    def __init__(self, error, *args: object) -> None:
        super().__init__(*args)

        self.err = error


def solve_captcha(driver: selenium.webdriver, iframe, t=5):
    """Solve the given captcha

#### Args:
    `driver` (`selenium.webdriver`): The active webdriver instance
    `iframe` (`any`): A reference to the captcha's iframe
    `t` (`int`, optional): Page load timeout (in seconds). Defaults to 5.

#### Returns:
        `Tuple(int, str)`: Error code (0 on success) and the answer (empty if error)
    """

    ret = None
    tmp_dir = tempfile.gettempdir()
    mp3_file = os.path.join(tmp_dir, "_tmp.mp3")
    wav_file = os.path.join(tmp_dir, "_tmp.wav")
    tmp_files = [mp3_file, wav_file]

    # Switch current context
    driver.switch_to.frame(iframe)

    # Click the checkbox
    wait_for_elem(driver, By.CLASS_NAME,
                  "recaptcha-checkbox-border", t).click()

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
        download_link = is_elem_present(
            driver, By.CLASS_NAME, "rc-audiochallenge-tdownload-link", t)

        if not download_link:
            raise NotExistent(status.RATELIMITED)

        with open(mp3_file, "wb") as f:
            link = download_link.get_attribute("href")
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

        # Return the text used for the answer
        ret = (status.SUCCESS, text)

    except TimeoutException as e:
        ret = (status.TIMEOUT, "")

    except NotExistent as e:
        # If we encounter the "Your computer is sending automated requests...", catch here and return the appropriate error
        ret = (e.err, "")

    except Exception as e:
        print(e)
        ret = (status.UNKNOWN, "")

    finally:
        __cleanup(tmp_files)
        return ret


def __cleanup(files: list):
    for x in files:
        if os.path.exists(x):
            os.remove(x)


def wait_for_elem(driver: selenium.webdriver, locator_type: str, locator: str, timeout: int):
    """
    Simple wrapper around selenium's find_element -- added a simple mechanism to wait until the element we want is present. Use try/except with `selenium.common.exceptions.TimeoutException`
    """
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((locator_type, locator)))


def is_elem_present(driver: selenium.webdriver, locator_type: str, locator: str, timeout: int):
    """
    Check if an element is present or wait for a timeout. Return the element if present otherwise False
    """
    try:
        return wait_for_elem(driver, locator_type, locator, timeout)
    except TimeoutException:
        return False
