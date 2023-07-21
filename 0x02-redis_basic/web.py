#!/usr/bin/env python3
"""
create a web cach
"""
import redis
import requests
from functools import wraps

rc = redis.Redis()

def cache_page(func):
    """ get a page and cach value"""
    @wraps(func)
    def wrapper(url):
        cached_value = rc.get(f"cached:{url}")
        if cached_value is not None:
            return cached_value.decode('utf-8')

        page_content = func(url)

        # Cache the page content with a 10-second expiration
        rc.setex(f"cached:{url}", 10, page_content)

        # Increment the access count for the URL
        rc.incr(f"count:{url}")

        return page_content

    return wrapper

@cache_page
def get_page(url: str) -> str:
    """ Get a page and cache the value"""
    resp = requests.get(url)
    return resp.text

if __name__ == "__main__":
    # Test the get_page function with caching
    page_content = get_page('http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com')
    print(page_content)
