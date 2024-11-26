#!/usr/bin/env python3

import os
import re
import json
import asyncio
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set, Any
from urllib.parse import urljoin, urlparse
from dotenv import load_dotenv
import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup
import requests
from firecrawl import FirecrawlApp

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TextScraper:
    def __init__(self, base_dir: str = "text_scrapes"):
        self.base_dir = Path(base_dir)
        self.firecrawl_api_key = os.getenv('FIRECRAWL_API_KEY')
        if not self.firecrawl_api_key:
            raise ValueError("FIRECRAWL_API_KEY not found in environment variables")
            
        # Initialize FireCrawl SDK
        self.firecrawl = FirecrawlApp(api_key=self.firecrawl_api_key)
        
        # Initialize regular session for fallback
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Create necessary directories
        self.base_dir.mkdir(exist_ok=True)
        self.metadata_dir = self.base_dir / "metadata"
        self.metadata_dir.mkdir(exist_ok=True)
        
        # Enhanced content type directories
        self.content_dirs = {
            'books': self.base_dir / "books",
            'articles': self.base_dir / "articles",
            'blog_posts': self.base_dir / "blog_posts"
        }
        for dir_path in self.content_dirs.values():
            dir_path.mkdir(exist_ok=True)
            
        # Initialize metadata selectors
        self._metadata_selectors = {
            'author': [
                'meta[name="author"]',
                'meta[property="article:author"]',
                '.author-name',
                '.byline'
            ],
            'date': [
                'meta[name="published_time"]',
                'meta[property="article:published_time"]',
                'time[datetime]',
                '.publish-date'
            ],
            'title': [
                'meta[property="og:title"]',
                'meta[name="twitter:title"]',
                'h1.entry-title',
                'h1.article-title'
            ]
        }
        
        # Initialize content selectors
        self._content_selectors = [
            'article',
            'main',
            '.content',
            '#article-content',
            '.post-content',
            '.entry-content'
        ]
        
    async def initialize(self):
        """Initialize the text scraper."""
        try:
            # Initialize aiohttp session
            self.aio_session = aiohttp.ClientSession()
            
            # Initialize cache directory
            self.cache_dir = Path("./data/scraper_cache")
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            
            # Load any cached data
            self.url_cache = {}
            self.quality_scores = {}
            self._load_cache()
            
            logging.info("Text scraper initialized successfully")
            
        except Exception as e:
            logging.error(f"Failed to initialize text scraper: {str(e)}")
            raise

    async def cleanup(self):
        """Cleanup resources."""
        try:
            if hasattr(self, 'aio_session') and self.aio_session and not self.aio_session.closed:
                try:
                    await asyncio.wait_for(self.aio_session.close(), timeout=2.0)
                except asyncio.TimeoutError:
                    logging.warning("Session cleanup timed out")
                except Exception as e:
                    logging.error(f"Error closing session: {str(e)}")
            
            # Save any pending cache updates
            try:
                await self._save_cache()
            except Exception as e:
                logging.error(f"Error saving cache during cleanup: {str(e)}")
                
            logging.info("Text scraper cleanup completed")
            
        except Exception as e:
            logging.error(f"Error during text scraper cleanup: {str(e)}")
            
    def _load_cache(self):
        """Load cached data from disk."""
        try:
            cache_file = self.cache_dir / "url_cache.json"
            if cache_file.exists():
                with open(cache_file, 'r') as f:
                    cached_data = json.load(f)
                    self.url_cache = cached_data.get('urls', {})
                    self.quality_scores = cached_data.get('scores', {})
        except Exception as e:
            logging.warning(f"Failed to load scraper cache: {str(e)}")

    async def _save_cache(self):
        """Save cache to disk."""
        try:
            cache_file = self.cache_dir / "url_cache.json"
            with open(cache_file, 'w') as f:
                json.dump({
                    'urls': self.url_cache,
                    'scores': self.quality_scores
                }, f)
        except Exception as e:
            logging.warning(f"Failed to save scraper cache: {str(e)}")

    def _is_text_content(self, url: str) -> bool:
        """Check if URL potentially contains text content."""
        text_indicators = [
            '/article/', '/blog/', '/post/', '/book/',
            '.txt', '.pdf', '.doc', '.docx', '.epub'
        ]
        return any(indicator in url.lower() for indicator in text_indicators)
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text content."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        return text.strip()
    
    def _extract_metadata(self, soup: BeautifulSoup, url: str) -> Dict:
        """Extract metadata from the webpage."""
        metadata = {
            'url': url,
            'scraped_at': datetime.now().isoformat(),
            'title': None,
            'author': None,
            'date_published': None,
            'content_type': None
        }
        
        # Try to extract title
        title_tag = soup.find('meta', property='og:title') or soup.find('title')
        if title_tag:
            metadata['title'] = title_tag.get('content', '') or title_tag.string
            
        # Try to extract author
        author_tag = soup.find('meta', property='author') or soup.find('meta', name='author')
        if author_tag:
            metadata['author'] = author_tag.get('content', '')
            
        # Try to extract publication date
        date_tag = soup.find('meta', property='article:published_time')
        if date_tag:
            metadata['date_published'] = date_tag.get('content', '')
            
        # Determine content type
        if '/article/' in url or '/news/' in url:
            metadata['content_type'] = 'articles'
        elif '/blog/' in url or '/post/' in url:
            metadata['content_type'] = 'blog_posts'
        elif '/book/' in url or url.endswith(('.pdf', '.epub')):
            metadata['content_type'] = 'books'
        else:
            metadata['content_type'] = 'articles'  # default
            
        return metadata
    
    async def _download_text(self, session: ClientSession, url: str) -> Tuple[str, Dict]:
        """Download and extract text content from a URL."""
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    logger.error(f"Failed to download {url}: Status {response.status}")
                    return None, None
                    
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extract main content
                # Remove script and style elements
                for element in soup(['script', 'style', 'nav', 'header', 'footer']):
                    element.decompose()
                
                # Extract text from main content areas
                content_tags = soup.find_all(['article', 'main', 'div'], class_=re.compile(r'content|article|post|text'))
                if not content_tags:
                    content_tags = [soup.body] if soup.body else [soup]
                
                text_content = []
                for tag in content_tags:
                    text_content.append(tag.get_text())
                
                text = ' '.join(text_content)
                cleaned_text = self._clean_text(text)
                
                # Extract metadata
                metadata = self._extract_metadata(soup, url)
                
                return cleaned_text, metadata
                
        except Exception as e:
            logger.error(f"Error downloading {url}: {str(e)}")
            return None, None
    
    async def get_content_with_firecrawl(self, url: str) -> Optional[str]:
        """Get content using FireCrawl SDK with fallback to direct requests."""
        try:
            logger.info("Attempting to scrape with FireCrawl...")
            # Use FireCrawl's scrape_url method with minimal parameters
            result = self.firecrawl.scrape_url(
                url,
                params={'formats': ['html']}
            )
            
            if result and 'html' in result:
                logger.info("Successfully retrieved content using FireCrawl")
                return result['html']
            
            logger.warning("FireCrawl returned no HTML content")
            return None
            
        except Exception as e:
            logger.error(f"FireCrawl error: {str(e)}")
            logger.info("Falling back to direct request...")
            
            # Fallback to direct request
            try:
                async with aiohttp.ClientSession(headers=self.session.headers) as session:
                    async with session.get(url) as response:
                        if response.status != 200:
                            logger.error(f"Failed to access {url}: Status {response.status}")
                            return None
                        html_content = await response.text()
                        logger.info("Successfully retrieved content using direct request")
                        return html_content
            except Exception as direct_error:
                logger.error(f"Direct request error: {str(direct_error)}")
                return None

    async def scrape_urls(self, urls: List[str], max_concurrent: int = 5):
        """Scrape multiple URLs concurrently."""
        async with aiohttp.ClientSession(headers=self.session.headers) as session:
            tasks = []
            for url in urls:
                if self._is_text_content(url):
                    tasks.append(self._download_text(session, url))
                
            results = []
            for future in asyncio.as_completed(tasks):
                text, metadata = await future
                if text and metadata:
                    results.append((text, metadata))
            
            return results
    
    def save_content(self, text: str, metadata: Dict):
        """Save scraped content and metadata."""
        try:
            content_type = metadata.get('content_type', 'articles')
            content_dir = self.content_dirs[content_type]
            
            # Create filename from title or URL
            title = metadata.get('title', '')
            if not title:
                title = urlparse(metadata['url']).path.split('/')[-1]
            
            # Clean filename
            filename = re.sub(r'[^\w\s-]', '', title).strip().lower()
            filename = re.sub(r'[-\s]+', '-', filename)
            
            # Save text content
            text_path = content_dir / f"{filename}.txt"
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(text)
            
            # Save metadata
            metadata_path = self.metadata_dir / f"{filename}.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
                
            logger.info(f"Saved content to {text_path}")
            return text_path
            
        except Exception as e:
            logger.error(f"Error saving content: {str(e)}")
            return None
    
    async def crawl_nested_content(self, url: str, base_path: Path = None) -> Dict:
        """Crawl content that may have nested sections/chapters using FireCrawl with fallback."""
        try:
            logger.info(f"Crawling content from: {url}")
            
            # Get content using FireCrawl with fallback
            html_content = await self.get_content_with_firecrawl(url)
            if not html_content:
                logger.error("Failed to retrieve content")
                return None
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Try to get content title
            title = self._extract_title(soup, url)
            logger.info(f"Found title: {title}")
            
            if not base_path:
                base_path = self.content_dirs['books'] / self._clean_filename(title)
                base_path.mkdir(exist_ok=True)
                logger.info(f"Created directory: {base_path}")
            
            # Look for nested sections/chapters
            sections = self._find_nested_sections(soup, url)
            
            if sections:
                logger.info(f"Found {len(sections)} sections to process")
                metadata = {
                    'title': title,
                    'url': url,
                    'type': 'container',
                    'sections': [],
                    'scraped_at': datetime.now().isoformat()
                }
                
                # Process each section
                for section_num, (section_title, section_url) in enumerate(sections, 1):
                    logger.info(f"Processing section {section_num}/{len(sections)}: {section_title}")
                    section_path = base_path / f"{section_num:03d}_{self._clean_filename(section_title)}"
                    section_path.mkdir(exist_ok=True)
                    
                    # Add a small delay between requests
                    if section_num > 1:
                        await asyncio.sleep(1)
                    
                    section_data = await self.crawl_nested_content(section_url, section_path)
                    if section_data:
                        metadata['sections'].append(section_data)
                        logger.info(f"Successfully processed section {section_num}/{len(sections)}")
                    else:
                        logger.warning(f"Failed to process section {section_num}/{len(sections)}")
                
                logger.info(f"Completed processing all {len(sections)} sections")
                
            else:
                # This is a content page
                logger.info("Processing content page...")
                content = self._extract_chapter_content(soup)
                
                if not content:
                    logger.error("Failed to extract content from page")
                    return None
                
                metadata = {
                    'title': title,
                    'url': url,
                    'type': 'content',
                    'scraped_at': datetime.now().isoformat()
                }
                
                # Save content as markdown
                markdown_content = self._format_markdown(title, url, content)
                file_path = base_path / f"{self._clean_filename(title)}.md"
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                
                metadata['file_path'] = str(file_path.relative_to(self.base_dir))
                logger.info(f"Saved content to {file_path}")
            
            # Save metadata
            metadata_path = self.metadata_dir / f"{self._clean_filename(title)}.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"Saved metadata to {metadata_path}")
            return metadata
            
        except Exception as e:
            logger.error(f"Error crawling {url}: {str(e)}")
            return None
    
    def _extract_title(self, soup: BeautifulSoup, url: str) -> str:
        """Extract title from the page."""
        # Try multiple title patterns
        title = None
        patterns = [
            ('h1', {}),
            ('title', {}),
            ('meta', {'property': 'og:title'}),
            ('div', {'class': 'title'}),
        ]
        
        for tag, attrs in patterns:
            element = soup.find(tag, attrs)
            if element:
                title = element.get('content', '') if tag == 'meta' else element.get_text()
                if title:
                    break
        
        if not title:
            # Extract from URL if no title found
            title = url.rstrip('/').split('/')[-1].replace('-', ' ').title()
        
        return title.strip()
    
    def _find_nested_sections(self, soup: BeautifulSoup, base_url: str) -> List[Tuple[str, str]]:
        """Find nested sections or chapters in the page."""
        sections = []
        
        # Common patterns for navigation/content links
        nav_patterns = [
            {'class_': re.compile(r'nav|menu|toc|contents|chapters', re.I)},
            {'id': re.compile(r'nav|menu|toc|contents|chapters', re.I)},
            {'role': 'navigation'}
        ]
        
        # Try to find navigation container
        for pattern in nav_patterns:
            nav = soup.find(['nav', 'div', 'ul'], pattern)
            if nav:
                break
        
        if not nav:
            nav = soup  # Fall back to entire page if no nav found
        
        # Find all links that might be sections
        for link in nav.find_all('a', href=True):
            href = link['href']
            if href.startswith(('#', 'javascript:')):
                continue
                
            url = urljoin(base_url, href)
            if url.startswith(base_url):  # Only include links from same domain
                title = link.get_text().strip()
                if title:
                    sections.append((title, url))
        
        return sections
    
    def _extract_chapter_content(self, soup: BeautifulSoup) -> str:
        """Extract the main content from a chapter page and format as markdown."""
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            element.decompose()
        
        # Try to find the main content container
        content_containers = soup.find_all(
            ['article', 'main', 'div'], 
            class_=re.compile(r'content|chapter|text|body')
        )
        
        if not content_containers:
            content_containers = [soup.body] if soup.body else [soup]
        
        markdown_content = []
        for container in content_containers:
            # Convert HTML elements to Markdown
            for h in container.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                level = int(h.name[1])
                h.replace_with(f"\n{'#' * level} {h.get_text().strip()}\n")
            
            for p in container.find_all('p'):
                p.replace_with(f"\n{p.get_text().strip()}\n")
            
            for ul in container.find_all('ul'):
                for li in ul.find_all('li'):
                    li.replace_with(f"* {li.get_text().strip()}\n")
            
            for ol in container.find_all('ol'):
                for i, li in enumerate(ol.find_all('li'), 1):
                    li.replace_with(f"{i}. {li.get_text().strip()}\n")
            
            for quote in container.find_all('blockquote'):
                lines = quote.get_text().strip().split('\n')
                quote.replace_with('\n'.join(f"> {line.strip()}" for line in lines if line.strip()))
            
            for em in container.find_all('em'):
                em.replace_with(f"_{em.get_text().strip()}_")
            
            for strong in container.find_all('strong'):
                strong.replace_with(f"**{strong.get_text().strip()}**")
            
            # Get the text and clean it
            text = container.get_text('\n', strip=True)
            if text:
                markdown_content.append(text)
        
        return '\n\n'.join(markdown_content)
    
    def _format_markdown(self, title: str, url: str, content: str) -> str:
        """Format content as markdown with frontmatter."""
        return f"""---
title: {title}
source: {url}
date_scraped: {datetime.now().isoformat()}
---

# {title}

{content}
"""

    def _clean_filename(self, text: str) -> str:
        """Create a clean filename from text."""
        # Remove invalid characters and clean up the text
        clean = re.sub(r'[^\w\s-]', '', text).strip().lower()
        return re.sub(r'[-\s]+', '-', clean)

    async def find_relevant_urls(self, query: str, max_urls: int = 5) -> List[str]:
        """Find relevant URLs for a given query."""
        try:
            # Initialize results
            results = []
            
            # Use multiple search strategies
            search_strategies = [
                self._search_web,
                self._search_cached_content,
                self._search_predefined_sources
            ]
            
            for strategy in search_strategies:
                try:
                    urls = await strategy(query, max_urls=max_urls)
                    results.extend(urls)
                    if len(results) >= max_urls:
                        break
                except Exception as e:
                    logging.warning(f"Search strategy failed: {str(e)}")
                    continue
            
            # Deduplicate and limit results
            results = list(dict.fromkeys(results))[:max_urls]
            
            if not results:
                logging.warning(f"No relevant URLs found for query: {query}")
            
            return results
            
        except Exception as e:
            logging.error(f"Error finding relevant URLs: {str(e)}")
            return []

    async def _search_web(self, query: str, max_urls: int = 5) -> List[str]:
        """Search the web for relevant content."""
        try:
            # Implement your preferred search method here
            # For now, return an empty list as we haven't implemented the actual search
            return []
        except Exception as e:
            logging.error(f"Web search failed: {str(e)}")
            return []

    async def _search_cached_content(self, query: str, max_urls: int = 5) -> List[str]:
        """Search through cached content."""
        try:
            relevant_urls = []
            for url, content in self.url_cache.items():
                if any(term.lower() in content.lower() for term in query.split()):
                    relevant_urls.append(url)
                    if len(relevant_urls) >= max_urls:
                        break
            return relevant_urls
        except Exception as e:
            logging.error(f"Cache search failed: {str(e)}")
            return []

    async def _search_predefined_sources(self, query: str, max_urls: int = 5) -> List[str]:
        """Search through predefined trusted sources."""
        try:
            # Add your predefined sources here
            trusted_sources = [
                "https://en.wikipedia.org/wiki/",
                "https://docs.python.org/3/",
                "https://developer.mozilla.org/en-US/docs/"
            ]
            
            relevant_urls = []
            for base_url in trusted_sources:
                if len(relevant_urls) >= max_urls:
                    break
                try:
                    search_url = f"{base_url}{query.replace(' ', '_')}"
                    async with self.aio_session.head(search_url) as response:
                        if response.status == 200:
                            relevant_urls.append(search_url)
                except:
                    continue
                    
            return relevant_urls
            
        except Exception as e:
            logging.error(f"Predefined source search failed: {str(e)}")
            return []
    
    async def update_source_relevance(self, url: str, score: float):
        """Update relevance score for a source."""
        metadata_file = self.metadata_dir / f"{self._get_safe_filename(url)}.json"
        if metadata_file.exists():
            metadata = json.loads(metadata_file.read_text())
            metadata['relevance_score'] = score
            metadata['last_updated'] = datetime.now().isoformat()
            metadata_file.write_text(json.dumps(metadata, indent=2))

    async def adjust_scraping_patterns(self, feedback: Dict[str, Any]):
        """Adjust scraping patterns based on feedback."""
        if feedback.get('missing_content'):
            self._update_content_patterns()
        if feedback.get('incorrect_metadata'):
            self._update_metadata_patterns()

    def _update_content_patterns(self):
        """Update content extraction patterns."""
        new_selectors = [
            'article',
            'main',
            '.content',
            '#article-content',
            '.post-content',
            '.entry-content'
        ]
        for selector in new_selectors:
            if selector not in self._content_selectors:
                self._content_selectors.append(selector)

    def _update_metadata_patterns(self):
        """Update metadata extraction patterns."""
        new_patterns = {
            'author': [
                'meta[name="author"]',
                'meta[property="article:author"]',
                '.author-name',
                '.byline'
            ],
            'date': [
                'meta[name="published_time"]',
                'meta[property="article:published_time"]',
                'time[datetime]',
                '.publish-date'
            ],
            'title': [
                'meta[property="og:title"]',
                'meta[name="twitter:title"]',
                'h1.entry-title',
                'h1.article-title'
            ]
        }
        for key, patterns in new_patterns.items():
            if key not in self._metadata_selectors:
                self._metadata_selectors[key] = []
            self._metadata_selectors[key].extend(
                [p for p in patterns if p not in self._metadata_selectors[key]]
            )

    def get_content_quality_score(self, content: str) -> float:
        """Calculate a quality score for the scraped content."""
        if not content:
            return 0.0
            
        # Basic quality metrics
        metrics = {
            'length': len(content) / 1000,  # Normalized by 1000 chars
            'sentence_count': len(content.split('. ')),
            'word_count': len(content.split()),
            'avg_word_length': sum(len(w) for w in content.split()) / len(content.split()) if content.split() else 0
        }
        
        # Quality indicators
        indicators = {
            'has_punctuation': bool(re.search(r'[.,!?]', content)),
            'has_paragraphs': content.count('\n\n') > 0,
            'proper_capitalization': bool(re.search(r'[A-Z][a-z]', content)),
            'no_excessive_spacing': not bool(re.search(r'\s{3,}', content))
        }
        
        # Calculate final score (0.0 to 1.0)
        base_score = min(1.0, (
            metrics['length'] * 0.3 +
            (metrics['sentence_count'] / 50) * 0.2 +
            (metrics['word_count'] / 500) * 0.3 +
            (metrics['avg_word_length'] / 10) * 0.2
        ))
        
        # Apply penalties for failed indicators
        penalty = sum(0.1 for indicator in indicators.values() if not indicator)
        final_score = max(0.0, base_score - penalty)
        
        return final_score

    async def process_url(self, url: str) -> Dict[str, Any]:
        """Process a URL and return structured data with quality metrics."""
        try:
            content = await self.scrape_url(url)
            if not content:
                return None
                
            chunks = self.chunk_content(content)
            quality_score = self.get_content_quality_score(content)
            
            return {
                'url': url,
                'content': chunks,
                'quality_score': quality_score,
                'metadata': self._extract_metadata(url),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Error processing URL {url}: {str(e)}")
            return None

async def main_async():
    """Main async function."""
    try:
        # Get URL from command line arguments or prompt
        if len(sys.argv) > 1:
            url = sys.argv[1].strip()
        else:
            url = input("Enter the URL to scrape (e.g., https://vedabase.io/en/library/bg/): ").strip()

        if not url:
            logger.error("No URL provided")
            return

        logger.info(f"Starting to crawl: {url}")
        scraper = TextScraper()
        await scraper.initialize()
        await scraper.crawl_nested_content(url)
        await scraper.cleanup()

    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")
    except Exception as e:
        logger.error(f"Failed to crawl {url}: {str(e)}")

def main():
    """Main function."""
    asyncio.run(main_async())

if __name__ == "__main__":
    main()
