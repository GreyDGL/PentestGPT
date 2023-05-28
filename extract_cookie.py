import platform
from pycookiecheat import chrome_cookies
import requests
import pprint

url = 'https://chat.openai.com/public-api/conversation_limit'

# Determine the operating system
os_name = platform.system()

if os_name == "Darwin":  # macOS
    cookie_file = "~/Library/Application Support/Google/Chrome/Profile 2/Cookies"
elif os_name == "Linux":
    cookie_file = "~/.config/google-chrome/Profile 2/Cookies"
else:
    raise Exception("Unsupported operating system: " + os_name)

cookies = chrome_cookies(url, cookie_file=cookie_file)

cookies_string = "; ".join(f"{k}={v}" for k, v in cookies.items())
print(cookies_string)
