"""Module for link data and metadata"""
from typing import Optional, Tuple
import requests
from bs4 import BeautifulSoup

def fetch_metadata(url) -> Tuple[Optional[str], Optional[str]]:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').get_text(strip=True) if soup.find('title') else 'No Title'
        description = soup.find('meta', attrs={'name': 'description'})
        if description:
            description = description.get('content', 'No Description').strip()
        else:
            description = 'No Description'
        return title, description
    except Exception as e:
        print(f"Failed to fetch metadata: {e}")
        return None, None

# TODO: define data structure for handling links rather than just the dictionary?