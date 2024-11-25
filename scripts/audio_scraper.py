#!/usr/bin/env python3

import os
import re
import json
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
from urllib.parse import urljoin, urlparse
from dotenv import load_dotenv

import aiohttp
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from aiohttp import ClientSession

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AudioScraper:
    def __init__(self, base_dir: str = "audio_scrapes"):
        self.base_dir = Path(base_dir)
        self.firecrawl_api_key = os.getenv('FIRECRAWL_API_KEY')
        if not self.firecrawl_api_key:
            raise ValueError("FIRECRAWL_API_KEY not found in environment variables")
            
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Authorization': f'Bearer {self.firecrawl_api_key}'
        })
        
        # Create necessary directories
        self.base_dir.mkdir(exist_ok=True)
        self.metadata_dir = self.base_dir / "metadata"
        self.metadata_dir.mkdir(exist_ok=True)
        
    def _is_audio_link(self, url: str) -> bool:
        audio_extensions = ('.mp3', '.wav', '.ogg', '.m4a', '.wma', '.aac')
        return url.lower().endswith(audio_extensions)
    
    def _sanitize_filename(self, filename: str) -> str:
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        filename = filename.replace(' ', '_')
        return filename.lower()
    
    def _extract_date(self, text: str) -> Optional[str]:
        date_patterns = [
            r'\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}',
            r'\d{4}-\d{2}-\d{2}',
            r'\d{2}/\d{2}/\d{4}'
        ]
        
        for pattern in date_patterns:
            if match := re.search(pattern, text):
                return match.group()
        return None
    
    def _crawl_with_firecrawl(self, url: str) -> Dict:
        try:
            api_url = "https://api.firecrawl.com/scrape"
            payload = {
                "url": url,
                "javascript": True,
                "wait_for": "audio,video",
                "extract_audio": True,
                "extract_metadata": True
            }
            
            response = self.session.post(api_url, json=payload)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"Firecrawl API error: {str(e)}")
            return {}

    async def _download_file_async(self, session: ClientSession, url: str, filepath: Path, description: str = "", progress_bars: Dict[str, tqdm] = None) -> bool:
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    logger.error(f"Error downloading {url}: HTTP {response.status}")
                    return False

                file_size = int(response.headers.get('content-length', 0))
                
                if filepath.name not in progress_bars:
                    progress_bars[filepath.name] = tqdm(
                        desc=filepath.name,
                        total=file_size,
                        unit='iB',
                        unit_scale=True,
                        unit_divisor=1024,
                    )

                pbar = progress_bars[filepath.name]
                
                with open(filepath, 'wb') as f:
                    async for chunk in response.content.iter_chunked(8192):
                        f.write(chunk)
                        pbar.update(len(chunk))

            metadata = {
                'url': url,
                'filename': filepath.name,
                'description': description,
                'download_date': datetime.now().isoformat(),
                'file_size': file_size
            }
            
            metadata_path = self.metadata_dir / f"{filepath.stem}_metadata.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            logger.error(f"Error downloading {url}: {str(e)}")
            if filepath.exists():
                filepath.unlink()
            return False
        finally:
            if filepath.name in progress_bars:
                progress_bars[filepath.name].close()
                del progress_bars[filepath.name]

    async def _download_all_files_async(self, audio_urls: Set[str], scrape_dir: Path, crawl_data: Dict) -> Tuple[int, int]:
        successful = 0
        total = len(audio_urls)
        progress_bars = {}

        async with aiohttp.ClientSession(headers=self.session.headers) as session:
            tasks = []
            for audio_url in audio_urls:
                context = next(
                    (audio.get('description', '') 
                     for audio in crawl_data.get('audio', [])
                     if audio.get('url') == audio_url),
                    ''
                )
                
                date_str = self._extract_date(context)
                prefix = f"{date_str}_" if date_str else ""
                
                filename = self._sanitize_filename(Path(audio_url).stem)
                filepath = scrape_dir / f"{prefix}{filename}{Path(audio_url).suffix}"
                
                logger.info(f"Queuing download: {filename}")
                task = self._download_file_async(session, audio_url, filepath, context, progress_bars)
                tasks.append(task)

            # Download files concurrently with a limit of 5 simultaneous downloads
            for i in range(0, len(tasks), 5):
                batch = tasks[i:i+5]
                results = await asyncio.gather(*batch, return_exceptions=True)
                successful += sum(1 for r in results if r is True)

        return successful, total
    
    async def scrape_page_async(self, url: str) -> Tuple[int, int]:
        try:
            logger.info(f"Fetching page: {url}")
            
            # First try Firecrawl API
            crawl_data = self._crawl_with_firecrawl(url)
            
            # Create scrape directory
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            domain = urlparse(url).netloc
            scrape_dir = self.base_dir / f"{domain}_{timestamp}"
            scrape_dir.mkdir(exist_ok=True)
            
            # Save page content and Firecrawl metadata
            page_content = {
                'url': url,
                'scrape_date': datetime.now().isoformat(),
                'firecrawl_data': crawl_data
            }
            
            with open(scrape_dir / "page_content.json", 'w', encoding='utf-8') as f:
                json.dump(page_content, f, indent=2, ensure_ascii=False)
            
            # Track unique audio URLs
            audio_urls: Set[str] = set()
            
            # Add audio URLs from Firecrawl data
            if 'audio' in crawl_data:
                for audio in crawl_data.get('audio', []):
                    if 'url' in audio:
                        audio_urls.add(audio['url'])
            
            # Fallback to traditional scraping if needed
            if not audio_urls:
                logger.info("Falling back to traditional scraping method")
                response = self.session.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for link in soup.find_all('a', href=True):
                    href = link.get('href')
                    full_url = urljoin(url, href)
                    if self._is_audio_link(full_url):
                        audio_urls.add(full_url)
            
            # Download files asynchronously
            return await self._download_all_files_async(audio_urls, scrape_dir, crawl_data)
            
        except Exception as e:
            logger.error(f"Error scraping page {url}: {str(e)}")
            return 0, 0

async def main_async():
    print("\nAudio Scraper Tool")
    print("------------------------")
    
    while True:
        url = input("\nEnter URL to scrape (or 'q' to quit): ").strip()
        
        if url.lower() == 'q':
            break
            
        if not url.startswith(('http://', 'https://')):
            print("Please enter a valid URL starting with http:// or https://")
            continue
        
        try:
            scraper = AudioScraper()
            successful, total = await scraper.scrape_page_async(url)
            
            print(f"\nScraping complete!")
            print(f"Downloaded {successful} of {total} files")
            print(f"Files saved in: {scraper.base_dir.absolute()}")
        except ValueError as e:
            print(f"Error: {str(e)}")
            print("Please make sure FIRECRAWL_API_KEY is set in your .env file")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()
