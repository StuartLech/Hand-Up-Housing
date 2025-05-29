import requests
from bs4 import BeautifulSoup
from .models import Listing
import json

# Example IHDA rent caps by bedroom count (placeholder values)
IHDA_RENT_CAPS = {
    0: 1000,
    1: 1200,
    2: 1400,
    3: 1600,
    4: 1800,
}

def parse_listings(soup):
    """Parse HTML and return a list of listing data dicts."""
    parsed = []
    for item in soup.select('.listing'):
        try:
            data = {
                'street': item.select_one('.street').get_text(strip=True),
                'city': item.select_one('.city').get_text(strip=True),
                'state': item.select_one('.state').get_text(strip=True),
                'zip': item.select_one('.zip').get_text(strip=True),
                'bedrooms': int(item.select_one('.bedrooms').get_text()),
                'bathrooms': int(item.select_one('.bathrooms').get_text()),
                'property_type': item.select_one('.property_type').get_text(strip=True).lower(),
                'lease_term': int(item.select_one('.lease_term').get_text()),
                'hud_subsidy': item.select_one('.hud').get_text(strip=True).lower(),
                'rent': int(item.select_one('.rent').get_text().replace('$', '').replace(',', '')),
            }
        except Exception:
            continue
        parsed.append(data)
    return parsed

def passes_requirements(data):
    if data.get('lease_term', 0) < 12:
        return False
    if 'hud' in data.get('hud_subsidy', '') or 'section 8' in data.get('hud_subsidy', ''):
        return False
    bedrooms = data.get('bedrooms', 0)
    rent = data.get('rent')
    cap = IHDA_RENT_CAPS.get(bedrooms, IHDA_RENT_CAPS[max(IHDA_RENT_CAPS.keys())])
    if rent is not None and rent > cap:
        return False
    return True

def create_listing(data):
    fields = {
        'street': data.get('street'),
        'city': data.get('city'),
        'state': data.get('state'),
        'zip': data.get('zip'),
        'bedrooms': data.get('bedrooms', 1),
        'bathrooms': data.get('bathrooms', 1),
        'property_type': data.get('property_type', 'house'),
    }
    listing, created = Listing.objects.get_or_create(**fields)
    return created, listing

def scrape_urls(urls):
    """Fetch each URL and create listings. Returns messages for display."""
    messages = []
    for url in urls:
        messages.append(f'Scraping {url}...')
        try:
            html = requests.get(url, timeout=10).text
        except Exception as exc:
            messages.append(f'Failed to fetch {url}: {exc}')
            continue
        soup = BeautifulSoup(html, 'html.parser')
        listings = parse_listings(soup)
        for data in listings:
            if passes_requirements(data):
                created, listing = create_listing(data)
                if created:
                    messages.append(f'Created listing at {listing}')
                else:
                    messages.append(f'Listing already exists: {listing}')
    messages.append('Scraping complete.')
    return messages


def scrape_api(api_url, api_key=None):
    """Fetch listing data from an API endpoint and create listings."""
    messages = []
    headers = {}
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'
    try:
        resp = requests.get(api_url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:
        messages.append(f'Failed to fetch {api_url}: {exc}')
        return messages

    if not isinstance(data, list):
        messages.append('API did not return a list of listings.')
        return messages

    for item in data:
        try:
            listing_data = {
                'street': item.get('street'),
                'city': item.get('city'),
                'state': item.get('state'),
                'zip': item.get('zip'),
                'bedrooms': int(item.get('bedrooms', 0)),
                'bathrooms': int(item.get('bathrooms', 1)),
                'property_type': str(item.get('property_type', 'house')).lower(),
                'lease_term': int(item.get('lease_term', 0)),
                'hud_subsidy': str(item.get('hud_subsidy', '')).lower(),
                'rent': int(item.get('rent', 0)),
            }
        except Exception:
            continue

        if passes_requirements(listing_data):
            created, listing = create_listing(listing_data)
            if created:
                messages.append(f'Created listing at {listing}')
            else:
                messages.append(f'Listing already exists: {listing}')

    if not messages:
        messages.append('No eligible listings found.')
    return messages
