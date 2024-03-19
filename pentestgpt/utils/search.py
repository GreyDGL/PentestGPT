# This file contains the utility function for performing searches online.
import requests
from newspaper import Article


def parse_url_with_newspaper(url: str) -> str:
    """
    This function parses the content of a URL using the newspaper library.
    :param url: the URL to parse
    :return: the content of the URL, main body only.
    """
    article = Article(url)
    article.download()
    article.parse()
    return article.text


def google_search_keyword_openserp(keyword: str, top_n=2) -> list:
    """
    This function performs a Google search via openserp.
    :param keyword: the keyword to search
    :return: a list of search results in the format of [(title, link), (title, link), ...]
        return [(None, None)] if no search results are found
    """
    # maintain a blacklist of websites that should not be included in the search results
    blacklist = ["medium.com", "github.com"]
    # example query: GET http://127.0.0.1:7001/google/search?lang=EN&limit=20&text=hello%20world
    url = f"http://127.0.0.1:7001/google/search?lang=EN&limit=10&text={keyword}"
    try:
        response = requests.get(url).json()
    except Exception as e:
        print(f"Request failed: {e}")
        return [(None, None)]
    # get the top n search results on the current page
    search_result = []
    i = 0
    while len(search_result) < top_n and i < len(response):
        try:
            # if any elements in the blacklist are in the link, skip the link
            if any([item in response[i]["url"] for item in blacklist]):
                i += 1
                continue
            search_results = response[i]
            search_result.append((search_results["title"], search_results["url"]))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            i += 1
    return search_result


def crawl_search(search_results: list) -> list:
    """
    This function crawls the search results into a JSON string as RAG.
    :param search_results: the search results returned by `search_online`
        the search result should be in the format of [(title, link), (title, link), ...]
        the search result should be as [None, None] if no search results are found
    :return: a list of strings as RAG
    """
    rag = []
    for title, link in search_results:
        # each website info is in the format of {title: "title", link: "link", content: "content"}
        if title is None or link is None:
            continue

        try:
            main_content = parse_url_with_newspaper(link)
            rag.append({"title": title, "link": link, "content": main_content})
        except Exception as e:
            print(f"Request failed on {link}: {e}")
            rag.append(
                {"title": title, "link": link, "content": "Failed to retrieve content"}
            )
            continue
    return rag


def check_search_connection(backend="openserp"):
    """
    This function checks if the search backend is available.
    :param backend: the backend to use for searching.
        Default is "openserp".
        Availables are "google" and "openserp"
    """
    if backend == "google":
        # TODO: add a test for the search feature
        return False
    elif backend == "openserp":
        # perform a get request to localhost:7001
        try:
            response = requests.get("http://localhost:7001/google/search?text=test")
            return response.status_code == 200
        except Exception:  # any exception can be handled as False
            return False
    else:
        return False


def search_as_RAG(list_of_keywords: list, backend="openserp") -> list:
    """
    This function searches the list of keywords and returns the search results as RAG.
    :param list_of_keywords: a list of keywords to search
    :param backend: the backend to use for searching.
        Default is "openserp".
        Availables are "google" and "openserp"
    """
    rag = []
    for keyword in list_of_keywords:
        if backend == "openserp":
            search_results = google_search_keyword_openserp(keyword)
        else:
            search_results = google_search_keyword_openserp(keyword)
        rag.extend(crawl_search(search_results))
    return rag


if __name__ == "__main__":
    # pre-check: check connection
    connection_status = check_search_connection()
    print("Connection Status:", connection_status)
    if connection_status:
        # test 1: search with openserp
        result = google_search_keyword_openserp("SQL Injection Tricks")
        print(result)

        # test 2: crawl information with openserp
        rag = search_as_RAG(["SQL Injection Tricks", "XSS Injection Tricks"])
        print(rag)
        for item in rag:
            print(item["title"], item["link"])

    else:
        print("The search docker is not up. Please start the search docker.")
