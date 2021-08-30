# python-captcha-bypass

[![License](https://img.shields.io/github/license/threadexio/python-captcha-bypass?style=for-the-badge)](https://github.com/threadexio/python-captcha-bypass/blob/master/LICENSE)
[![Tests](https://img.shields.io/travis/com/threadexio/python-captcha-bypass?label=Tests&logo=python&logoColor=yellow&style=for-the-badge)](https://app.travis-ci.com/github/threadexio/python-captcha-bypass)

A small and harmless utility written in Python used to solve CAPTCHAs with Selenium.

# How to use

1. Clone this repo
```bash
git clone https://github.com/threadexio/python-captcha-bypass
```

2. Copy `src/captcha_bypass.py` to your project

3. Import with `from captcha_bypass import solve_captcha`

-------

# Dependencies:
- python3

- chromium (or Google Chrome, others might work but are not tested)
  * Windows:  `https://www.chromium.org/getting-involved/download-chromium`
  * Linux:
    - Debian-based: `sudo apt-get install chromium`
    - Arch-based:   `sudo pacman -S chromium`
    - Fedora-based: `sudo dnf install chromium`

- ffmpeg
  * Windows:  `https://www.ffmpeg.org/download.html`
  * Linux:
    - Debian-based: `sudo apt-get install ffmpeg`
    - Arch-based:   `sudo pacman -S ffmpeg`
    - Fedora-based: `sudo dnf install ffmpeg`

-------

# Docs

```python
solve_captcha(browser, captcha)
```
`browser`: is the active webdriver instance (`selenium.webdriver`)

`captcha`: is a reference to the CAPTCHA's iframe

### See `src/test.py` for a code example

-------

### Legal Disclaimer
This was made for educational purposes only, nobody directly involved in this project is responsible for any damages caused. You are responsible for your actions
