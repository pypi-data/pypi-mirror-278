from cd_multi_tasker.cd_multi_tasker import MultiTasking

"""
This can be used for a list of urls, proxies, meme tokens, crypto currencies and so on
Just note that url could proxy, token, currency.
Max workers means connections. You don't want too many connections to one url unless under a proxy.
"""

multitasker = MultiTasking(max_workers=4)


# Example task function for HTTP requests (placeholder)
def fetch_data(url):
    """
    Dummy function to simulate fetching data from a URL.
    Replace with actual HTTP request logic.

    Parameters:
        url (str): URL to fetch data from.

    Returns:
        str: Dummy response message.

        This is where you process the data.
    """
    return f"Fetched data from {url}"


# Example list of URLs to fetch data from
urls = ["http://example.com/data1", "http://example.com/data2"]
results = multitasker.run_io_bound_tasks(urls, fetch_data)
print("HTTP fetching results:", results)
