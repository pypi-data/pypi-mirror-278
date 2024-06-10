# ValidLink

A simple Python library to check the validity of URLs.

## Features

- Check the validity of a given URL.
- Automatically add missing schemes (e.g., `http://`).
- Handle URLs without common subdomains like `www.`.
- Graceful error handling for various request exceptions.

## Installation

```bash
pip install validlink
```

## Usage

### Basic Usage

```python
from validlink import check_url_validity

url = "https://www.example.com"
is_valid = check_url_validity(url)
if is_valid:
    print(f"The URL {url} is valid.")
else:
    print(f"The URL {url} is not valid.")
```

### Handling Different URL Formats

```python
from validlink import check_url_validity

urls = [
    "example.com",
    "http://example.com",
    "https://example.com",
    "www.example.com",
    "example.com/test",
]

for url in urls:
    is_valid = check_url_validity(url)
    if is_valid:
        print(f"The URL {url} is valid.")
    else:
        print(f"The URL {url} is not valid.")
```

### Extracting URLs from Messages

```python
from validlink import find_urls_in_message, check_url_validity

messages = [
    "your message Eid code good https://www.example.com thank you god",
    "your message Eid code good example.com thank you god",
]

for message in messages:
    urls = find_urls_in_message(message)
    for url in urls:
        is_valid = check_url_validity(url)
        if is_valid:
            print(f"The URL {url} found in the message is valid.")
        else:
            print(f"The URL {url} found in the message is not valid.")
```

### Checking URLs from User Input

```python
from validlink import check_url_validity

url = input("Enter a URL to check: ")
is_valid = check_url_validity(url)
if is_valid:
    print(f"The URL {url} is valid.")
else:
    print(f"The URL {url} is not valid.")
```

### Handling URLs in Web Scraping

```python
import requests
from validlink import check_url_validity

# Assume urls_list contains a list of URLs obtained from web scraping
urls_list = ["https://www.example.com", "http://example.com", "www.example.com"]

for url in urls_list:
    is_valid = check_url_validity(url)
    if is_valid:
        print(f"The URL {url} is valid.")
    else:
        print(f"The URL {url} is not valid.")
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgements

Special thanks to all the contributors of open-source libraries that made this project possible.

## Thank You

Thank you to all users who have found this tool helpful! Your support and feedback are greatly appreciated. ❤️🎈
