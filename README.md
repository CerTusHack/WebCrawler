# Web Crawler for Bug Hunting Automation

This Python script is designed to automate the process of web crawling and form submission for bug bounty hunting. It utilizes asynchronous programming with asyncio and aiohttp to achieve concurrent HTTP requests and form submissions.

## Features

1. **Web Crawling**: The script recursively crawls through the specified domain, discovering internal links and identifying forms on web pages.
2. **Form Detection**: It detects HTML forms on crawled web pages and logs their URLs.
3. **Form Submission**: For each discovered form, the script can perform a form submission with specified data.
4. **Sensitive Directories**: It detects sensitive directories on crawled web pages.
5. **External resources**: It also detects external resources.
6. **Throttling**: It includes a rate-limiting mechanism to avoid overloading the server with too many concurrent requests.
7. **Error Handling**: The script handles errors gracefully and logs them for debugging purposes.

## Usage

### Clone the Repository: Clone the repository containing the script.

 git clone https://github.com/CerTusHack/WebCrawler.git

### Install Dependencies: Install the required dependencies using pip.

pip install -r requirements.txt

(Make sure you have installed pip)
### Run the Script: Execute the script and provide the domain you want to crawl when prompted.

python CertCrawler.py

## Customization

1. **Maximum Depth**: Adjust the `max_depth` variable to control the maximum recursion depth for crawling.
2. **Concurrent Requests**: Modify the `concurrent_requests` variable to change the number of concurrent HTTP requests.
3. **Crawl Delay**: Set the `crawl_delay` variable to control the delay between consecutive requests to avoid overloading the server.

## Contributing

Contributions, bug reports, and feature requests are welcome! Feel free to open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
