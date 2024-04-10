# Web Crawler for Bug Bounty Automation

This Python script is designed to automate the process of web crawling and form submission for bug bounty hunting. It utilizes asynchronous programming with asyncio and aiohttp to achieve concurrent HTTP requests and form submissions.

## Features

1. **Web Crawling**: The script recursively crawls through the specified domain, discovering internal links and identifying forms on web pages.
2. **Form Detection**: It detects HTML forms on crawled web pages and logs their URLs.
3. **Form Submission**: For each discovered form, the script can perform a form submission with specified data.
4. **Throttling**: It includes a rate-limiting mechanism to avoid overloading the server with too many concurrent requests.
5. **Error Handling**: The script handles errors gracefully and logs them for debugging purposes.

## Usage

1. **Installation**: Make sure you have Python 3.x installed on your system. Install required dependencies using `pip install -r requirements.txt`.
2. **Execution**: Run the script by executing `python web_crawler.py`.
3. **Input**: Enter the domain you want to crawl when prompted. The script will start crawling from the specified domain.
4. **Output**: The script logs information about discovered forms and form submissions. Execution time is also displayed upon completion.

## Customization

1. **Maximum Depth**: Adjust the `max_depth` variable to control the maximum recursion depth for crawling.
2. **Concurrent Requests**: Modify the `concurrent_requests` variable to change the number of concurrent HTTP requests.
3. **Crawl Delay**: Set the `crawl_delay` variable to control the delay between consecutive requests to avoid overloading the server.

## Contributing

Contributions, bug reports, and feature requests are welcome! Feel free to open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
