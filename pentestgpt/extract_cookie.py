import os
import platform
import pprint
from pathlib import Path

import requests
from pycookiecheat import chrome_cookies
from rich.console import Console


def main():
    console = Console()
    url = "https://chat.openai.com/public-api/conversation_limit"

    # Determine the operating system
    os_name = platform.system()
    cookie_file = os.getenv("BROWSER_COOKIE_DB")
    if not cookie_file:
        home = str(Path.home())
        if os_name == "Darwin":  # macOS
            cookie_file = Path(
                home, "Library/Application Support/Google/Chrome/Profile 2/Cookies"
            )
        elif os_name == "Linux":
            cookie_file = Path(home, ".config/google-chrome/Default/Cookies")
        else:
            raise Exception("Unsupported operating system: " + os_name)

    if os.path.isfile(cookie_file):
        cookies = chrome_cookies(url, cookie_file=cookie_file)
        cookies_string = "; ".join(f"{k}={v}" for k, v in cookies.items())
        console.print("Run the following command to set the cookie:\n")
        console.print("export CHATGPT_COOKIE='" + cookies_string + "'")
    else:
        console.print(
            "Please run this script on the same machine with Chrome installed and/or"
            "set BROWSER_COOKIE_DB to point to your cookies db "
            "(e.g. 'export BROWSER_COOKIE_DB=~/.config/google-chrome/Profile 2/Cookies').",
            style="bold yellow",
        )


if __name__ == "__main__":
    main()
