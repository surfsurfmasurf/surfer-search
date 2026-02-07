import argparse
from src.crawler.base_crawler import BaseCrawler
from src.parser.html_parser import HTMLParser
import json

def main():
    parser = argparse.ArgumentParser(description="Surfer Search Crawler Test")
    parser.add_argument("url", help="URL to crawl")
    args = parser.parse_args()

    crawler = BaseCrawler()
    html_parser = HTMLParser()

    print(f"Crawling: {args.url}")
    content = crawler.fetch(args.url)
    
    if content:
        print("Parsing content...")
        parsed_data = html_parser.parse(content, args.url)
        
        # Display structured result
        print(json.dumps(parsed_data, indent=2, ensure_ascii=False))
    else:
        print("Failed to fetch content.")

if __name__ == "__main__":
    main()
