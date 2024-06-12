[![PyPI](https://img.shields.io/badge/Version-1.0.1-blue.svg)](https://github.com/SlowWave/ProxyMana)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<br/>
<p align="center">
  <a href="https://github.com/SlowWave/ProxyMana">
    <img src="https://raw.githubusercontent.com/SlowWave/ProxyMana/main/docs/images/proxymana_logo.png" alt="Logo" width="100" height="100">
  </a>

  <h3 align="center">ProxyMana</h3>
</p>


## Table Of Contents

- [Table Of Contents](#table-of-contents)
- [About The Project](#about-the-project)
- [Features](#features)
  - [Summary of Configurable Parameters](#summary-of-configurable-parameters)
- [Installation](#installation)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [Detailed Example](#detailed-example)
- [License](#license)


## About The Project

ProxyMana is a straightforward and easy-to-use proxy management tool designed to periodically search for and manage free anonymous proxies from [SSL Proxies](https://www.sslproxies.org/). It simplifies the process of proxy rotation by automating the discovery, validation, and management of proxies, making it an ideal solution for applications that require reliable and anonymous web scraping or data fetching.

ProxyMama scraping utilities are based on the [free-proxy](https://github.com/jundymek/free-proxy/) tool, a very useful tool for scraping free proxies from several providers.


## Features

Despite its simplicity, ProxyMana provides a range of useful features:

- **Periodic Proxy Search**:
  - ProxyMana automatically searches for new free proxies at regular intervals by scraping the [SSL Proxies](https://www.sslproxies.org/) website. This ensures that you always have a fresh set of proxies to use.

- **Simple Management of Available and Invalid Proxies**:
  - The class maintains two lists: one for available proxies and another for invalid proxies. This helps in efficiently managing and rotating proxies without reusing invalid ones.

- **Easy Scheduler Thread Management**:
  - ProxyMana includes simple methods to start and stop a scheduler thread. The scheduler runs in the background, periodically updating the list of available proxies and clearing out invalid ones.

- **Fetching and Removing Proxies Made Easy**:
  - You can fetch a new proxy from the list of available proxies using the `get_new_proxy` method. If a proxy is invalid, you can remove it from the list using the `remove_proxy` method. This ensures that only functional proxies are used in your application.


### Summary of Configurable Parameters

- `proxy_timeout`: Sets the timeout value for checking proxy validity.
- `proxy_search_freq`: Defines how often (in seconds) the tool searches for new proxies.
- `proxy_clear_freq`: Determines how often (in seconds) the list of invalid proxies is cleared.


## Installation

To install ProxyMana library use:

```
pip install proxymana
```
## Usage

### Basic Usage

1. Import the ProxyMana class:

``` python
from proxymana.proxymana import ProxyMana
```

2. Start the scheduler thread:

``` python
ProxyMana.start_scheduler_thread(
    proxy_timeout=1, 
    proxy_search_freq=1, 
    proxy_clear_freq=120, 
    verbose=True
)
```

3. Get a new proxy:

``` python
proxy = ProxyMana.get_new_proxy()
print(f"New proxy: {proxy}")
```

4. Remove an invalid proxy:

``` python
ProxyMana.remove_proxy(proxy)
```

5. Stop the scheduler thread:

``` python
ProxyMana.stop_scheduler_thread()
```

### Detailed Example

This example demonstrates how to use the ProxyMana class to manage and utilize proxies for making HTTP requests to multiple target URLs in a multithreaded environment. The example includes starting a scheduler to periodically update and clear proxies, and running threads to fetch content from specified websites using these proxies.

``` python
import requests
import threading
import time

from proxymana.proxymana import ProxyMana

# Initialize the list of target URLs
TARGET_URLS = [
    "https://www.twitter.com/",
    "https://www.linkedin.com/",
    "https://www.instagram.com/"
]

# Define the function that each thread will run
def fetch_content(url):
    while True:
        # Get a new proxy from ProxyMana
        proxy = ProxyMana.get_new_proxy()
        if proxy:
            try:
                # Make the HTTP request using the proxy
                response = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=10)
                if response.status_code == 200:
                    print(f"Successfully fetched content from {url} using proxy {proxy}")
                    # Break the loop if the request is successful
                    break
                else:
                    print(f"Failed to fetch content from {url} using proxy {proxy}")
                    # Remove the invalid proxy
                    ProxyMana.remove_proxy(proxy)
            except Exception as e:
                print(f"Error fetching content from {url} using proxy {proxy}: {e}")
                # Remove the invalid proxy
                ProxyMana.remove_proxy(proxy)
        else:
            print("No proxies available, retrying...")
            time.sleep(1)

# Start the ProxyMana scheduler thread
ProxyMana.start_scheduler_thread(
    proxy_timeout=2,
    proxy_search_freq=1,
    proxy_clear_freq=120,
    verbose=True
)

# Create and start threads for each URL
threads = []
for url in TARGET_URLS:
    thread = threading.Thread(target=fetch_content, args=(url,))
    thread.start()
    threads.append(thread)

# Wait for all threads to complete
for thread in threads:
    thread.join()

# Stop the ProxyMana scheduler thread when done
ProxyMana.stop_scheduler_thread()
```


## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.