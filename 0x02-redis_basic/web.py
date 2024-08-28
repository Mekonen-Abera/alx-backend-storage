import requests
import time
from functools import wraps

# Cache dictionary to store URL responses and their access counts
cache = {}
access_count = {}

def cache_with_expiration(expiration_time: int):
    """Decorator to cache function results with expiration."""
    def decorator(func):
        @wraps(func)
        def wrapper(url: str):
            # Check if the URL is in the cache
            if url in cache:
                cached_time, cached_value = cache[url]
                # If the cache is still valid, return the cached value
                if time.time() - cached_time < expiration_time:
                    return cached_value
            
            # If the cache is expired or not present, call the function
            result = func(url)
            # Update the cache with the current time and result
            cache[url] = (time.time(), result)
            return result
        return wrapper
    return decorator

@cache_with_expiration(10)
def get_page(url: str) -> str:
    """Fetches the HTML content of a URL and tracks access count."""
    # Increment access count
    if f'count:{url}' in access_count:
        access_count[f'count:{url}'] += 1
    else:
        access_count[f'count:{url}'] = 1
    
    # Fetch the page content
    response = requests.get(url)
    return response.text

# Example usage
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/10000/url/http://www.example.com"
    
    # Fetch the page multiple times to test caching
    print(get_page(url))  # First fetch, should take time
    print(get_page(url))  # Second fetch within 10 seconds, should be cached
    time.sleep(11)        # Wait for cache to expire
    print(get_page(url))  # Third fetch, should take time again
    print(access_count)    # Print access counts

