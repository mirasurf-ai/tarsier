"""
Utility functions for Tarsier.
"""

from typing import Optional
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from crawl4ai import Page


def is_pdf_or_image(url: str) -> bool:
    """Check if URL points to a PDF or image file."""
    parsed = urlparse(url)
    path = parsed.path.lower()
    return any(path.endswith(ext) for ext in ['.pdf', '.jpg', '.jpeg', '.png', '.gif'])


def extract_text_content(page: Page, output_format: str = "text") -> Optional[str]:
    """
    Extract text content from a web page.
    
    Args:
        page: Crawl4ai Page object
        output_format: Output format ('text' or 'markdown')
        
    Returns:
        Extracted content in specified format
    """
    soup = BeautifulSoup(page.html, 'html.parser')
    
    # Remove unwanted elements
    for element in soup.find_all(['script', 'style', 'nav', 'footer', 'header']):
        element.decompose()
    
    if output_format == "markdown":
        # Convert to markdown (basic implementation)
        content = []
        for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li']):
            if element.name.startswith('h'):
                level = int(element.name[1])
                content.append(f"{'#' * level} {element.get_text().strip()}")
            elif element.name == 'p':
                content.append(element.get_text().strip())
            elif element.name == 'li':
                content.append(f"- {element.get_text().strip()}")
        return "\n\n".join(content)
    else:
        # Plain text
        return soup.get_text(separator='\n', strip=True) 