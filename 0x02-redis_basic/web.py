#!/usr/bin/env python3
"""
Create a web cache.
"""
import redis
import requests

# Initialize Redis client
rc = redis.Redis()

def get_page(url: str) -> str:
    """Fetch a page and cache its value."""
    # Check if the page is already cached
    cached_page = rc.get(f"cached:{url}")
    
    if cached_page:
        # If cached, return the cached value
        print("Returning cached value.")
        return cached_page.decode('utf-8')

    # If not cached, fetch the page
    print("Fetching new page.")
    resp = requests.get(url)

    # Store the fetched page in cache with an expiration time of 10 seconds
    rc.setex(f"cached:{url}", 10, resp.text)
    rc.incr(f"count:{url}")  # Increment access count
    return resp.text

if __name__ == "__main__":
    page_content = get_page('http://slowwly.robertomurray.co.uk')
    print(page_content)

