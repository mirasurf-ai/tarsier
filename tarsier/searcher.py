"""
Core searcher functionality for Tarsier.
"""

import os
from typing import List, Optional, Union, Dict
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from crawl4ai import Browser
from meilisearch import Client as MeiliClient
from qdrant_client import QdrantClient
from unstructured.partition.auto import partition

from .utils import extract_text_content, is_pdf_or_image


class TarsierSearcher:
    """Main class for web search and data extraction."""

    def __init__(
        self,
        meili_url: str = "http://localhost:7700",
        meili_key: Optional[str] = None,
        qdrant_url: str = "http://localhost:6333",
        qdrant_key: Optional[str] = None,
        proxy: Optional[Dict[str, str]] = None,
    ):
        """
        Initialize the searcher with storage clients.
        
        Args:
            meili_url: Meilisearch server URL
            meili_key: Meilisearch API key
            qdrant_url: Qdrant server URL
            qdrant_key: Qdrant API key
            proxy: Proxy configuration dictionary. Example:
                  {
                      "http": "http://proxy.example.com:8080",
                      "https": "http://proxy.example.com:8080"
                  }
        """
        self.browser = Browser(proxy=proxy)
        self.meili_client = MeiliClient(meili_url, meili_key)
        self.qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_key)
        
        # Initialize indices
        self._init_indices()

    def _init_indices(self):
        """Initialize Meilisearch and Qdrant indices."""
        # Meilisearch index
        if "pages" not in self.meili_client.get_indexes():
            self.meili_client.create_index("pages", {"primaryKey": "url"})
        
        # Qdrant collection
        self.qdrant_client.recreate_collection(
            collection_name="pages",
            vectors_config={"size": 1536, "distance": "Cosine"}
        )

    def search(
        self,
        query: str,
        output_format: str = "text",
        max_results: int = 10
    ) -> List[dict]:
        """
        Search the web and extract content from results.
        
        Args:
            query: Search query string
            output_format: Output format ('text' or 'markdown')
            max_results: Maximum number of results to process
            
        Returns:
            List of dictionaries containing URL and extracted content
        """
        # Search Google using headless browser
        search_results = self.browser.search_google(query, max_results=max_results)
        results = []

        for url in search_results:
            try:
                content = self._extract_content(url, output_format)
                if content:
                    # Store in Meilisearch
                    self.meili_client.index("pages").add_documents([{
                        "url": url,
                        "content": content,
                        "query": query
                    }])
                    
                    # Store in Qdrant
                    self.qdrant_client.upsert(
                        collection_name="pages",
                        points=[{
                            "id": url,
                            "vector": self._get_embedding(content),
                            "payload": {
                                "url": url,
                                "content": content,
                                "query": query
                            }
                        }]
                    )
                    
                    results.append({
                        "url": url,
                        "content": content
                    })
            except Exception as e:
                print(f"Error processing {url}: {str(e)}")
                continue

        return results

    def _extract_content(self, url: str, output_format: str) -> Optional[str]:
        """Extract content from a URL."""
        try:
            if is_pdf_or_image(url):
                # Download and process PDF/image
                response = requests.get(url)
                elements = partition(file=response.content)
                content = "\n".join([str(el) for el in elements])
            else:
                # Use browser to fetch and extract content
                page = self.browser.get(url)
                content = extract_text_content(page, output_format)
            
            return content
        except Exception as e:
            print(f"Error extracting content from {url}: {str(e)}")
            return None

    def _get_embedding(self, text: str) -> List[float]:
        """Get embedding vector for text (placeholder implementation)."""
        # TODO: Implement proper embedding generation
        return [0.0] * 1536  # Placeholder vector 