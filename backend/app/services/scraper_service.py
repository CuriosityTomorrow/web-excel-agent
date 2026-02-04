import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from app.models.excel import Sheet


class ScraperService:
    def scrape_table(self, url: str, table_index: int = 0) -> Sheet:
        """
        Scrape a table from a webpage
        Returns a Sheet object that can be used to create an Excel workbook
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            tables = soup.find_all('table')

            if table_index >= len(tables):
                raise ValueError(f"Table index {table_index} not found. Only {len(tables)} tables available.")

            table = tables[table_index]
            rows = []

            # Extract table data
            for row in table.find_all('tr'):
                cells = []
                for cell in row.find_all(['td', 'th']):
                    text = cell.get_text(strip=True)
                    cells.append(text)
                if cells:
                    rows.append(cells)

            if not rows:
                raise ValueError("No data found in table")

            # Ensure all rows have the same number of columns
            max_cols = max(len(row) for row in rows)
            for row in rows:
                while len(row) < max_cols:
                    row.append('')

            sheet_name = f"Table_{table_index + 1}"
            return Sheet(name=sheet_name, rows=rows)

        except requests.RequestException as e:
            raise ValueError(f"Failed to fetch URL: {str(e)}")
        except Exception as e:
            raise ValueError(f"Failed to scrape table: {str(e)}")

    def scrape_list(self, url: str, list_index: int = 0) -> Sheet:
        """
        Scrape a list (ul/ol) from a webpage
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            lists = soup.find_all(['ul', 'ol'])

            if list_index >= len(lists):
                raise ValueError(f"List index {list_index} not found. Only {len(lists)} lists available.")

            list_elem = lists[list_index]
            rows = []

            for item in list_elem.find_all('li'):
                text = item.get_text(strip=True)
                rows.append([text])

            sheet_name = f"List_{list_index + 1}"
            return Sheet(name=sheet_name, rows=rows)

        except Exception as e:
            raise ValueError(f"Failed to scrape list: {str(e)}")


# Global instance
scraper_service = ScraperService()
