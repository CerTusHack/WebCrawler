import json
import os
import aiohttp
import asyncio
import time
import logging
import signal
import sys
from urllib.parse import urlparse, urljoin
from lxml import html as lh

# Configure logging
logging.basicConfig(format='%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define colors for different log levels
LOG_COLORS = {
    "INFO": "\033[94m",  # Blue
    "WARNING": "\033[93m",  # Yellow
    "ERROR": "\033[91m",  # Red
    "DEBUG": "\033[92m",  # Green
    "RESET": "\033[0m"  # Reset
}

print("""
╭─┬─┬───┬─┬──╮
│C│E│R│T│U│S │
╰─┴─┴───┴─┴──╯
""")

# Global variables
visited_urls = set()
max_depth = 3  # Maximum recursion depth

# Dictionary to cache IPinfo responses
ipinfo_cache = {}

async def main():
    connector = aiohttp.TCPConnector()
    async with aiohttp.ClientSession(connector=connector) as client:
        domain = input("Enter the domain you want to crawl (e.g., example.com): ")
        starting_url = "https://" + domain if not domain.startswith("https://") else domain
        await crawl(client, starting_url, 0)
        sensitive_directories = await get_sensitive_directories(client, starting_url)

async def crawl(client, url, depth):
    color = LOG_COLORS["INFO"]
    logger.info(f"{color}Analyzing URL: {url}{LOG_COLORS['RESET']}")
    if depth <= max_depth and url not in visited_urls:
        visited_urls.add(url)
        async with client.get(url) as response:
            html_content = await response.text()
            if html_content:
                tree = lh.fromstring(html_content)
                forms = tree.xpath('//form')
                input_texts = tree.xpath('//input[@type="text"]')
                if forms or input_texts:
                    logger.info(f"Scrape Found: {url}")
                internal_links = get_internal_links(url, html_content)
                await asyncio.gather(*[crawl(client, link, depth + 1) for link in internal_links])
                await check_external_resources(client, url, html_content)
                # Scraping data from the webpage
                scraped_data = scrape_data(url, html_content)
                if scraped_data:
                    logger.info(f"Scraped data from {url}: Title - {scraped_data['Title']}, Paragraphs count - {len(scraped_data['Paragraphs'])}")
                    export_to_json(scraped_data, f"{url.replace(':', '_').replace('/', '_')}.json")
                # Accessing data from a public API
                await access_ipinfo_api(url)

async def access_ipinfo_api(url):
    color = LOG_COLORS["INFO"]
    logger.info(f"{color}Working with IPinfo API...{LOG_COLORS['RESET']}")
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        
        # Check if IP info for this domain is cached
        if domain in ipinfo_cache:
            data = ipinfo_cache[domain]
            logger.info(f"IPinfo data (cached) for {url}: {data}")
        else:
            ipinfo_url = f"http://ip-api.com/json/{domain}"
            async with aiohttp.ClientSession() as session:
                async with session.get(ipinfo_url) as response:
                    data = await response.json()
                    logger.info(f"IPinfo data for {url}: {data}")
                    # Cache the IPinfo response
                    ipinfo_cache[domain] = data
    except Exception as e:
        logger.error(f"Error accessing IPinfo API: {e}")

async def get_sensitive_directories(client, url):
    color = LOG_COLORS["INFO"]
    logger.info(f"{color}Searching for sensitive directories...{LOG_COLORS['RESET']}")
    sensitive_directories = [
        ".git", ".svn", ".DS_Store", "CVS", "backup", "backups", "backup_files",
        "backup_files_old", "backup_files_old_versions", "backup_old", "backup_old_versions",
        "backup_old_files", "backup_old_versions_files", "old", "old_versions", "old_files",
        "old_versions_files", "test", "tests", "temp", "tmp", "logs", "log", "debug"
    ]
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    results = []
    async with client:
        for directory in sensitive_directories:
            test_url = f"{base_url}/{directory}"
            async with client.get(test_url) as response:
                if response.status == 200:
                    results.append(test_url)
    if results:
        logger.info(f"Sensitive directories found: {results}")
    else:
        logger.info("No sensitive directories found.")
    return results

async def check_external_resources(client, url, html_content):
    color = LOG_COLORS["INFO"]
    logger.info(f"{color}Checking external resources...{LOG_COLORS['RESET']}")
    tree = lh.fromstring(html_content)
    external_resources = {
        "JavaScript": tree.xpath('//script/@src'),
        "CSS": tree.xpath('//link[@rel="stylesheet"]/@href'),
        "Images": tree.xpath('//img/@src'),
        "Other": tree.xpath('//source/@src') + tree.xpath('//video/@src') + tree.xpath('//audio/@src')
    }
    for resource_type, resources in external_resources.items():
        if resources:
            logger.info(f"{resource_type} resources found on {url}: {resources}")
        else:
            logger.info(f"No {resource_type} resources found on {url}.")

def get_internal_links(url, html_content):
    tree = lh.fromstring(html_content)
    internal_links = tree.xpath('//a/@href')
    return [urljoin(url, link) for link in internal_links]

def scrape_data(url, html_content):
    color = LOG_COLORS["INFO"]
    logger.info(f"{color}Scraping data from {url}...{LOG_COLORS['RESET']}")
    try:
        tree = lh.fromstring(html_content)
        title = tree.xpath('//title/text()')[0].strip() if tree.xpath('//title/text()') else ""
        paragraphs = [p.strip() for p in tree.xpath('//p/text()') if p.strip()]
        form_links = tree.xpath('//form/@action')
        return {"Title": title, "Paragraphs": paragraphs, "Form Links": form_links}
    except Exception as e:
        logger.error(f"Error scraping data from {url}: {e}")
        return None

def export_to_json(data, filename):
    color = LOG_COLORS["INFO"]
    logger.info(f"{color}Data exported to {filename}{LOG_COLORS['RESET']}")
    with open(filename, "w") as f:
        json.dump(data, f)

def handle_interrupt(signal, frame):
    color = LOG_COLORS["WARNING"]
    logger.warning(f"{color}Program interrupted by user. Exiting...{LOG_COLORS['RESET']}")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_interrupt)
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    execution_time = round(end_time - start_time, 2)
    color = LOG_COLORS["INFO"]
    logger.info(f"{color}Execution time: {execution_time} seconds{LOG_COLORS['RESET']}")
