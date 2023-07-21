#!/usr/bin/env python3
"""
create a web cache
"""
import redis
import requests
rc = redis.Redis()


def get_page(url: str) -> str:
    """ get a page and cache value"""
    cached_value = rc.get(f"cached:{url}")
    if cached_value is not None:
        return cached_value.decode('utf-8')

    resp = requests.get(url)
    rc.setex(f"cached:{url}", 10, resp.text)  # Cache the page content with a 10-second expiration
    rc.incr(f"count:{url}")  # Increment the access count for the URL
    return resp.text


if __name__ == "__main__":
    page_content = get_page('http://slowwly.robertomurray.co.uk')
    print(page_content)
