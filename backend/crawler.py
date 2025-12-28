"""
Web crawler module for the RAG Ingestion Pipeline.

This module handles crawling of the Docusaurus site, extracting content,
and preparing it for further processing.
"""

import os
import time
import logging
import requests
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass
from bs4 import BeautifulSoup
import re
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


logger = logging.getLogger(__name__)


@dataclass
class CrawledPage:
    """Represents a crawled web page with its content and metadata."""
    url: str
    title: str
    content: str
    headings: List[Dict[str, Any]]
    links: List[str]


class Crawler:
    """Handles crawling of the Docusaurus site."""

    def __init__(self, base_url: str, user_agent: str = "RAG-Ingestion-Pipeline/1.0",
                 timeout: int = 30, delay: float = 0.1, max_retries: int = 3):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.session = self._create_session(max_retries, timeout)
        self.session.headers.update({
            'User-Agent': user_agent
        })
        self.timeout = timeout
        self.delay = delay
        self.max_retries = max_retries
        self.visited_urls = set()
        self.logger = logger

    def _create_session(self, max_retries: int, timeout: int) -> requests.Session:
        """Create a requests session with retry strategy."""
        session = requests.Session()

        # Define retry strategy
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def is_internal_link(self, url: str) -> bool:
        """Check if a URL is internal to the base domain."""
        url_domain = urlparse(url).netloc
        return url_domain == self.base_domain or url_domain.endswith('.' + self.base_domain)

    def extract_links(self, soup: BeautifulSoup, current_url: str) -> List[str]:
        """Extract all internal links from a page."""
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']

            # Skip anchor links and javascript links
            if href.startswith(('#', 'javascript:', 'mailto:')):
                continue

            full_url = urljoin(current_url, href)

            # Only include internal links from the same domain
            if self.is_internal_link(full_url):
                # Normalize URL by removing fragments
                full_url = full_url.split('#')[0]
                links.append(full_url)

        return list(set(links))  # Remove duplicates

    def clean_text(self, text: str) -> str:
        """Clean extracted text by removing extra whitespace."""
        # Remove multiple consecutive newlines and spaces
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r' +', ' ', text)
        return text.strip()

    def extract_headings(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract headings (h1-h6) from the page."""
        headings = []
        for i, heading in enumerate(soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])):
            headings.append({
                'level': int(heading.name[1]),  # Extract number from h1, h2, etc.
                'text': heading.get_text().strip(),
                'position': i
            })
        return headings

    def get_page_content(self, url: str) -> Optional[CrawledPage]:
        """Crawl a single page and extract its content."""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract title
            title_tag = soup.find('title')
            title = title_tag.get_text().strip() if title_tag else "No Title"

            # Remove script and style elements before extracting text
            for script in soup(["script", "style"]):
                script.decompose()

            # Extract main content (try to focus on main content areas)
            # Look for common content containers in Docusaurus sites
            main_content = (
                soup.find('main') or
                soup.find('article') or
                soup.find('div', class_='main') or
                soup.find('div', class_='container') or
                soup.find('div', class_='docItemContainer') or
                soup.find('div', class_='theme-doc-markdown') or
                soup
            )

            text_content = main_content.get_text()

            # Clean the extracted text
            cleaned_content = self.clean_text(text_content)

            # Extract headings and links
            headings = self.extract_headings(soup)
            links = self.extract_links(soup, url)

            return CrawledPage(
                url=url,
                title=title,
                content=cleaned_content,
                headings=headings,
                links=links
            )
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request error crawling {url}: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Error crawling {url}: {str(e)}")
            return None

    def crawl_site(self) -> List[CrawledPage]:
        """Crawl the entire site starting from the base URL."""
        self.logger.info(f"Starting crawl of {self.base_url}")

        # Start with the base URL
        urls_to_visit = [self.base_url]
        crawled_pages = []

        while urls_to_visit:
            current_url = urls_to_visit.pop(0)

            if current_url in self.visited_urls:
                continue

            self.logger.info(f"Crawling: {current_url}")
            self.visited_urls.add(current_url)

            page = self.get_page_content(current_url)
            if page:
                crawled_pages.append(page)

                # Add new internal links to the queue
                for link in page.links:
                    if link not in self.visited_urls and link not in urls_to_visit:
                        urls_to_visit.append(link)

            # Small delay to be respectful to the server
            time.sleep(self.delay)

        self.logger.info(f"Crawling completed. Total pages crawled: {len(crawled_pages)}")
        return crawled_pages

    def get_sitemap_urls(self) -> List[str]:
        """Try to get URLs from sitemap if available."""
        sitemap_url = urljoin(self.base_url, '/sitemap.xml')
        try:
            response = self.session.get(sitemap_url, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'xml')
            urls = []
            for loc in soup.find_all('loc'):
                url = loc.text.strip()
                if self.is_internal_link(url):
                    urls.append(url)
            self.logger.info(f"Found {len(urls)} URLs from sitemap")
            return urls
        except Exception as e:
            self.logger.info(f"No sitemap found or error accessing sitemap: {str(e)}")
            return []