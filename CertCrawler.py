import aiohttp
import asyncio
import time
import logging
from urllib.parse import urlparse, urljoin
from lxml import html as lh
import signal
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("""
╭─┬─┬───┬─┬──╮
│C│E│R│T│U│S │
╰─┴─┴───┴─┴──╯
""")

# Global variables
visited_urls = set()
max_depth = 3  # Maximum recursion depth
concurrent_requests = 10  # Number of concurrent requests
crawl_delay = 1  # Delay between requests to avoid overloading the server

async def fetch(url):
    logger.info(f"Fetching URL: {url}")
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, allow_redirects=True, timeout=10) as response:
                if response.status == 200:
                    logger.info("URL fetched successfully.")
                    return await response.text()
                else:
                    logger.warning(f"Failed to fetch URL. Status code: {response.status}")
                    return None
        except aiohttp.ClientError as e:
            logger.error(f"Error fetching URL {url}: {e}")
            return None

def get_internal_links(url, html_content):
    logger.info("Extracting internal links...")
    internal_links = set()
    tree = lh.fromstring(html_content)
    for link in tree.xpath('//a/@href'):
        next_url = urljoin(url, link)
        parsed_next_url = urlparse(next_url)
        if parsed_next_url.scheme and parsed_next_url.netloc == urlparse(url).netloc:
            internal_links.add(next_url)
    if internal_links:
        logger.info(f"Internal links found: {internal_links}")
    else:
        logger.info("No internal links found.")
    return internal_links

async def crawl(url, depth):
    logger.info(f"Crawling URL: {url}")
    if depth <= max_depth and url not in visited_urls:
        visited_urls.add(url)
        html_content = await fetch(url)
        if html_content:
            tree = lh.fromstring(html_content)
            forms = tree.xpath('//form')
            input_texts = tree.xpath('//input[@type="text"]')
            if forms or input_texts:
                logger.info(f"Form Found: {url}")
            internal_links = get_internal_links(url, html_content)
            await asyncio.gather(*[crawl(link, depth + 1) for link in internal_links])
            await check_external_resources(url, html_content)

async def get_sensitive_directories(url):
    logger.info("Searching for sensitive directories...")
    sensitive_directories = [
        ".git", ".svn", ".DS_Store", "CVS", "backup", "backups", "backup_files",
        "backup_files_old", "backup_files_old_versions", "backup_old", "backup_old_versions",
        "backup_old_files", "backup_old_versions_files", "old", "old_versions", "old_files",
        "old_versions_files", "test", "tests", "temp", "tmp", "logs", "log", "debug"
    ]
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    results = []
    async with aiohttp.ClientSession() as session:
        for directory in sensitive_directories:
            test_url = f"{base_url}/{directory}"
            async with session.get(test_url) as response:
                if response.status == 200:
                    results.append(test_url)
    if results:
        logger.info(f"Sensitive directories found: {results}")
    else:
        logger.info("No sensitive directories found.")
    return results

async def check_external_resources(url, html_content):
    logger.info("Checking external resources...")
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

async def main():
    domain = input("Enter the domain you want to crawl (e.g., example.com): ")
    starting_url = "https://" + domain if not domain.startswith("https://") else domain
    await crawl(starting_url, 0)
    sensitive_directories = await get_sensitive_directories(starting_url)

def handle_interrupt(sig, frame):
    logger.info("Scan interrupted by user.")
    sys.exit(0)

if __name__ == "__main__":
    start_time = time.time()
    signal.signal(signal.SIGINT, handle_interrupt)
    asyncio.run(main())
    logger.info(f"Execution time: {round(time.time() - start_time, 2)} seconds")
