from bs4 import BeautifulSoup
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HTMLParser:
    def __init__(self):
        pass

    def clean_text(self, text):
        """Remove extra whitespace and normalize text."""
        if not text:
            return ""
        return re.sub(r'\s+', ' ', text).strip()

    def extract_links(self, soup, base_url):
        """Extract all internal and external links."""
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            # Basic normalization (could be improved with urllib.parse.urljoin)
            if href.startswith('/'):
                # Handle relative paths (simplified)
                # In a real scenario, use urllib.parse.urljoin(base_url, href)
                pass 
            elif href.startswith('http'):
                links.add(href)
        return list(links)

    def parse(self, html_content, url):
        """
        Parse HTML content and return structured data.
        Returns:
            dict: {
                'title': str,
                'meta_description': str,
                'headings': list,
                'main_text': str,
                'links': list
            }
        """
        if not html_content:
            return None

        try:
            soup = BeautifulSoup(html_content, 'lxml')

            # 1. Title
            title = soup.title.string.strip() if soup.title and soup.title.string else ""

            # 2. Meta Description
            meta_desc = ""
            meta_tag = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
            if meta_tag and meta_tag.get('content'):
                meta_desc = meta_tag['content'].strip()

            # 3. Remove noise (scripts, styles, noscript)
            for element in soup(["script", "style", "noscript", "iframe", "header", "footer", "nav"]):
                element.decompose()

            # 4. Headings (H1-H3) for importance
            headings = []
            for h in soup.find_all(['h1', 'h2', 'h3']):
                text = self.clean_text(h.get_text())
                if text:
                    headings.append({'tag': h.name, 'text': text})

            # 5. Main Text Content
            # Get text and clean it
            main_text = self.clean_text(soup.get_text(separator=' '))

            # 6. Links
            links = self.extract_links(soup, url)

            return {
                'url': url,
                'title': title,
                'meta_description': meta_desc,
                'headings': headings,
                'content': main_text,
                'links': links
            }

        except Exception as e:
            logger.error(f"Error parsing HTML from {url}: {e}")
            return None
