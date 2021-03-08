# python-captcha-bypass

A small and harmless utility written in Python used to solve CAPTCHAs with Selenium.

# Tests
[![Build Status](https://travis-ci.com/threadexio/python-captcha-bypass.svg?branch=master)](https://travis-ci.com/threadexio/python-captcha-bypass)

# How to use

1. Clone this repo
```bash
git clone https://github.com/threadexio/python-captcha-bypass
```

2. Copy `src/captcha_bypass.py` to your project

3. Import with `from captcha_bypass import solve_captcha`

-------

# Docs

```python
solve_captcha(browser, captcha)
#				/\		  /\
#				||		  ||
#			Webdriver	 CAPTCHA iframe
#
```
### Where:
`browser`: is the active webdriver instance (`selenium.webdriver`)

`captcha`: is a reference to the CAPTCHA's iframe

-------

## See `src/test.py` for a code example
