import requests
from bs4 import BeautifulSoup


def g_search(query, num_results=1):
    """
    Parameters:
    - query (str): The search query to be used.
    - num_results (int, optional): The number of top results to retrieve (default is 1).

    Returns:
    str: A string containing the top search results.

    Note:
    This function performs a Google search using the provided query and retrieves
    the specified number of top results. It uses web scraping techniques to parse
    Google's search results page and extract relevant information.

    Example:
    >>> search_query = "Python programming"
    >>> top_results = google_search(search_query, num_results=3)
    >>> print(top_results)
    """
    try:
        search_url = f"https://www.google.com/search?q={query}"
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, "html.parser")

        search_results = soup.find_all("div", class_="BNeawe")
        top_results = [result.text for result in search_results[:num_results]]


        if not top_results:
            print("No results found")
        else:
            result_text = "\n\n".join(top_results)
            if len(result_text) < 10:
                more_results = g_search(query, num_results=5)  # Show next 5 results
                if more_results:
                    result_text += "\n".join(more_results)
            return result_text

    except Exception as e:
        return e
