import aiohttp
import asyncio
import time
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

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
    soup = BeautifulSoup(html_content, 'html.parser')
    for link in soup.find_all('a', href=True):
        next_url = urljoin(url, link['href'])
        parsed_next_url = urlparse(next_url)
        if parsed_next_url.scheme and parsed_next_url.netloc == urlparse(url).netloc:
            internal_links.add(next_url)
    return internal_links

async def crawl(url, depth):
    if depth <= max_depth and url not in visited_urls:
        visited_urls.add(url)
        html_content = await fetch(url)
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            forms = soup.find_all('form')
            input_texts = soup.find_all('input', {'type': 'text'})
            if forms or input_texts:
                logger.info(f"Form Found: {url}")
            internal_links = get_internal_links(url, html_content)
            await asyncio.gather(*[crawl(link, depth + 1) for link in internal_links])

async def process_form_submission(url, form_data):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, data=form_data, timeout=10) as response:
                if response.status == 200:
                    logger.info(f"Form submitted successfully: {url}")
                else:
                    logger.warning(f"Failed to submit form: {url}. Status code: {response.status}")
        except Exception as e:
            logger.error(f"Error submitting form: {url}. {e}")

async def main():
    domain = input("Enter the domain you want to crawl (e.g., example.com): ")
    starting_url = "https://" + domain if not domain.startswith("https://") else domain
    await crawl(starting_url, 0)

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    logger.info(f"Execution time: {round(time.time() - start_time, 2)} seconds")
