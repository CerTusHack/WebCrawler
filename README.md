# Web Crawler by CERTUSHACK

This is a web crawler tool designed to scan websites for vulnerabilities and sensitive information. It recursively crawls internal links, checks for sensitive directories, and identifies external resources such as JavaScript, CSS, images, and other files.

## Features

- Crawls internal links recursively up to a specified depth.
- Identifies forms and input fields on web pages.
- Searches for sensitive directories commonly found in web applications.
- Checks for external resources like JavaScript, CSS, images, and other files.
- Designed to be lightweight and efficient.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/CerTusHack/WebCrawler.git
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To use the web crawler, simply run the `main.py` script and follow the prompts:

```bash
python CertCrawler.py
```

Enter the domain you want to crawl when prompted, and the crawler will start scanning the website.

## Configuration

You can configure the maximum recursion depth and other parameters directly in the `CertCrawler.py` file by modifying the `max_depth` variable.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-new-feature`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-new-feature`).
6. Create a new Pull Request.

## License

This project is licensed under the GNU License. See the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for educational purposes only. Use it responsibly and with proper authorization. We are not responsible for any misuse or damage caused by this tool.
