import aiohttp
import asyncio
import time
import logging
from urllib.parse import urlparse, urljoin
from lxml import html as lh

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
visited_urls = set()
max_depth = 3  # Maximum recursion depth
concurrent_requests = 10  # Number of concurrent requests
crawl_delay = 1  # Delay between requests to avoid overloading the server

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, allow_redirects=True, timeout=10) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    return None
        except Exception as e:
            logger.error(f"Error fetching URL {url}: {e}")
            return None

def get_internal_links(url, html_content):
    internal_links = set()
    tree = lh.fromstring(html_content)
    for link in tree.xpath('//a/@href'):
        next_url = urljoin(url, link)
        parsed_next_url = urlparse(next_url)
        if parsed_next_url.scheme and parsed_next_url.netloc == urlparse(url).netloc:
            internal_links.add(next_url)
    return internal_links

async def crawl(url, depth):
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

async def main():
    domain = input("Enter the domain you want to crawl (e.g., example.com): ")
    starting_url = "https://" + domain if not domain.startswith("https://") else domain
    await crawl(starting_url, 0)

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    logger.info(f"Execution time: {round(time.time() - start_time, 2)} seconds")
