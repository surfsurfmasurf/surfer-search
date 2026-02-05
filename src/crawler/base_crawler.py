import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseCrawler:
    def __init__(self, user_agent=None):
        self.headers = {
            'User-Agent': user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        }

    def fetch(self, url):
        """Fetch the content of a URL."""
        try:
            logger.info(f"Fetching: {url}")
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    def parse_basic(self, html):
        """Parse basic metadata from HTML."""
        if not html:
            return None
        
        soup = BeautifulSoup(html, 'lxml')
        title = soup.title.string if soup.title else "No Title"
        
        # Remove script and style elements
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        # Get text
        text = soup.get_text(separator=' ', strip=True)
        
        return {
            'title': title,
            'content': text
        }

if __name__ == "__main__":
    # Test run
    crawler = BaseCrawler()
    sample_url = "https://example.com"
    content = crawler.fetch(sample_url)
    data = crawler.parse_basic(content)
    print(f"Result for {sample_url}:")
    print(f"Title: {data['title']}")
    print(f"Content snippet: {data['content'][:100]}...")
