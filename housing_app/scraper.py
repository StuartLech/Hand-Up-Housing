try:
    from bs4 import BeautifulSoup
except Exception:
    BeautifulSoup = None

from .models import Listing

# Example IHDA rent caps by bedroom count (placeholder values)
IHDA_RENT_CAPS = {
    0: 1000,
    1: 1200,
    2: 1400,
    3: 1600,
    4: 1800,
}

def fetch_html(url, timeout=10):
    """Fetch URL and return the HTML text."""
    try:
        import requests
    except Exception as exc:  # pragma: no cover - fallback when requests missing
        raise ImportError("The 'requests' package is required to scrape URLs") from exc

    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.text


def parse_listings(html):
    """Parse raw HTML and return a list of dicts for Listings."""
    if BeautifulSoup is None:
        raise ImportError("The 'beautifulsoup4' package is required to parse listings")
    soup = BeautifulSoup(html, "html.parser")
    parsed = []
    for item in soup.select(".listing"):
        try:
            data = {
                "street": item.select_one(".street").get_text(strip=True),
                "city": item.select_one(".city").get_text(strip=True),
                "state": item.select_one(".state").get_text(strip=True),
                "zip": item.select_one(".zip").get_text(strip=True),
                "bedrooms": int(item.select_one(".bedrooms").get_text()),
                "bathrooms": int(item.select_one(".bathrooms").get_text()),
                "property_type": item.select_one(".property_type").get_text(strip=True).lower(),
                # Extra fields for filtering
                "lease_term": int(item.select_one(".lease_term").get_text()),
                "hud_subsidy": item.select_one(".hud").get_text(strip=True).lower(),
                "rent": int(
                    item.select_one(".rent").get_text().replace("$", "").replace(",", "")
                ),
            }
        except Exception:
            continue
        parsed.append(data)
    return parsed


def passes_requirements(data):
    """Check lease term, HUD subsidy, and rent cap requirements."""
    if data.get("lease_term", 0) < 12:
        return False
    if "hud" in data.get("hud_subsidy", "") or "section 8" in data.get("hud_subsidy", ""):
        return False
    bedrooms = data.get("bedrooms", 0)
    rent = data.get("rent")
    cap = IHDA_RENT_CAPS.get(bedrooms, IHDA_RENT_CAPS[max(IHDA_RENT_CAPS.keys())])
    if rent is not None and rent > cap:
        return False
    return True


def create_listing(data):
    """Create a Listing object if it doesn't already exist."""
    fields = {
        "street": data.get("street"),
        "city": data.get("city"),
        "state": data.get("state"),
        "zip": data.get("zip"),
        "bedrooms": data.get("bedrooms", 1),
        "bathrooms": data.get("bathrooms", 1),
        "property_type": data.get("property_type", "house"),
    }
    listing, created = Listing.objects.get_or_create(**fields)
    return listing, created
