
# Web Crawler by CERTUSHACK

This is a Python web crawler script that extracts data from webpages and checks for sensitive directories.

## Dependencies

- Python 3.7 or higher
- aiohttp==3.9.2
- lxml==5.2.1

## Installation

1. Clone the repository:


git clone https://github.com/CertusHack/WebCrawler.git


2. Install the dependencies:


pip install -r requirements.txt


## Usage

1. Run the script:


python CertCrawler.py


2. Enter the domain you want to crawl when prompted.

3. Wait for the script to finish crawling the website. The extracted data will be saved in JSON files.


## Features

- Asynchronous HTTP requests: The module provides functionality for making asynchronous HTTP requests, allowing for efficient web crawling and data retrieval.
Support for asyncio: It seamlessly integrates with Python's asyncio framework, making it easy to write asynchronous code.

- TCPConnector: The module includes a TCPConnector class for managing TCP connections, providing options for configuring connection parameters.

- ClientSession: It offers a ClientSession class for managing HTTP sessions, which can be used to make multiple requests within the same session, allowing for better performance and resource management.

- Request and response handling: It provides classes and methods for handling HTTP requests and responses, including support for headers, cookies, and other request/response parameters.

- Exception handling: The module includes built-in exception handling for handling errors and exceptions that may occur during HTTP requests.

- URL parsing and manipulation: It offers utilities for parsing and manipulating URLs, such as urljoin and urlparse functions.

- Logging: The module supports logging, allowing developers to log debugging and diagnostic information.

- Signal handling: It includes functionality for handling signals, such as SIGINT, allowing for graceful termination of HTTP requests and sessions.

- Time measurement: The module includes utilities for measuring execution time, which can be useful for performance profiling and optimization.


## License

This project is licensed under the GNU License - see the [LICENSE](LICENSE) file for details.

