"""
MCP Tools for web scraping
These tools can be used by the AI Agent to scrape data from web pages
"""
from typing import Dict, Any
from app.services.scraper_service import scraper_service


def scrape_web_table(url: str, table_index: int = 0) -> Dict[str, Any]:
    """
    Scrape a table from a webpage

    Args:
        url: URL of the webpage to scrape
        table_index: Index of the table to scrape (default: 0, first table)

    Returns:
        Sheet data with scraped table content

    Example:
        >>> scrape_web_table("https://example.com", table_index=0)
    """
    sheet = scraper_service.scrape_table(url, table_index)
    return sheet.dict()


def scrape_web_list(url: str, list_index: int = 0) -> Dict[str, Any]:
    """
    Scrape a list (ul/ol) from a webpage

    Args:
        url: URL of the webpage to scrape
        list_index: Index of the list to scrape (default: 0, first list)

    Returns:
        Sheet data with scraped list content
    """
    sheet = scraper_service.scrape_list(url, list_index)
    return sheet.dict()


def extract_structured_data(url: str, selector: str = None) -> list:
    """
    Extract structured data from webpage using CSS selectors

    Args:
        url: URL of the webpage
        selector: CSS selector for elements to extract

    Returns:
        List of extracted data
    """
    import requests
    from bs4 import BeautifulSoup

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.content, 'html.parser')

    if selector:
        elements = soup.select(selector)
        return [elem.get_text(strip=True) for elem in elements]
    else:
        # Extract all text content
        return [soup.get_text(strip=True)]


# Register MCP tools
MCP_TOOLS = {
    'scrape_web_table': scrape_web_table,
    'scrape_web_list': scrape_web_list,
    'extract_structured_data': extract_structured_data,
}
