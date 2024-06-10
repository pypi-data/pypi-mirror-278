import requests
from urllib.parse import urlparse, urlunparse
import re

def check_url_validity(url):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = "http://" + url
        parsed_url = urlparse(url)

    if not parsed_url.netloc:
        parsed_url = urlparse("http://" + url)
    if not parsed_url.path:
        url = urlunparse(parsed_url._replace(path="/"))

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.HTTPError:
        return False
    except requests.exceptions.ConnectionError:
        return False
    except requests.exceptions.Timeout:
        return False
    except requests.exceptions.RequestException:
        return False

def find_urls_in_message(message):
    url_pattern = r'(https?://\S+)|(www\.\S+)'
    urls = re.findall(url_pattern, message)
    urls = [url[0] or url[1] for url in urls if url[0] or url[1]]
    return urls
      
