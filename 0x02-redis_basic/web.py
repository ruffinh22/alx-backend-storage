#!/usr/bin/env python3
"""
create a web cache
"""
import redis
import requests
from functools import wraps

rc = redis.Redis()

def cache_page(func):
    @wraps(func)
    def wrapper(url):
        # Check if the page is already cached
        cached_value = rc.get(f"cached:{url}")
        if cached_value is not None:
            print("Using cached content...")
            return cached_value.decode('utf-8')

        # Fetch the page content and cache it
        resp = requests.get(url)
        rc.setex(f"cached:{url}", 10, resp.text)

        # Increment the access count for the URL
        rc.incr(f"count:{url}")

        return resp.text

    return wrapper

@cache_page
def get_page(url: str) -> str:
    """ Get a page and cache the value"""
    return requests.get(url).text

if __name__ == "__main__":
    page_content = get_page('http://slowwly.robertomurray.co.uk')
    print(page_content)
