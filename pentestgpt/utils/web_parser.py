# Use functions from Auto-GPT: https://github.com/Torantulino/Auto-GPT/blob/master/scripts/browse.py
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from googlesearch import search

######### Quick documentation #########
## Use get response to get the original response from the URL
## Use parse_web to get the text from the URL (bs4 handled)
## Use google_search to get the search results from Google. Results are already parsed.
#######################################


# Function to check if the URL is valid
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


# Function to sanitize the URL
def sanitize_url(url):
    return urljoin(url, urlparse(url).path)


def check_local_file_access(url):
    local_prefixes = [
        "file:///",
        "file://localhost",
        "http://localhost",
        "https://localhost",
    ]
    return any(url.startswith(prefix) for prefix in local_prefixes)


def get_response(url, timeout=10) -> tuple:
    """
    Get the response from the URL.

    Parameters:
    ----------
        url (str): The URL to get the response from.
        timeout (int): The timeout for the HTTP request.

    Returns:
    -------
        response (requests.models.Response): The response from the URL.
        error (str): The error message if any.
    """
    try:
        # Restrict access to local files
        if check_local_file_access(url):
            raise ValueError("Access to local files is restricted")

        # Most basic check if the URL is valid:
        if not url.startswith("http://") and not url.startswith("https://"):
            raise ValueError("Invalid URL format")

        sanitized_url = sanitize_url(url)

        user_agent_header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        }

        response = requests.get(
            sanitized_url, headers=user_agent_header, timeout=timeout
        )

        # Check if the response contains an HTTP error
        if response.status_code >= 400:
            return None, f"Error: HTTP {response.status_code} error"

        return response, None
    except ValueError as ve:
        # Handle invalid URL format
        return None, f"Error: {str(ve)}"

    except requests.exceptions.RequestException as re:
        # Handle exceptions related to the HTTP request (e.g., connection errors, timeouts, etc.)
        return None, f"Error: {str(re)}"


def parse_web(url) -> str:
    # create a user agent header
    response, potential_error = get_response(url)
    if response is None:
        return potential_error

    # Check if the response contains an HTTP error
    if response.status_code >= 400:
        return f"Error: HTTP {str(response.status_code)} error"

    soup = BeautifulSoup(response.text, "html.parser")

    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = "\n".join(chunk for chunk in chunks if chunk)

    return text


def google_search(keyword, num_results=5) -> dict:
    """
    Search on Google and return the results.

    Parameters:
    ----------
        keyword (str): The keyword to search on Google.
        num_results (int): The number of results to return.

    Returns:
    -------
        result (dict): The search results. Format: {"keyword": keyword, "search_result": {url, content}}}

    """
    search_result = {
        url: parse_web(url)
        for url in search(
            keyword, tld="com", num=num_results, stop=num_results, pause=2
        )
    }
    return {"keyword": keyword, "search_result": search_result}


if __name__ == "__main__":
    # test to query google search on "what is penetration testing?"
    query = "what is penetration testing?"
    for url in search(query, tld="com", num=5, stop=5, pause=2):
        print(url)
        web_content = parse_web(url)
        print(web_content)
