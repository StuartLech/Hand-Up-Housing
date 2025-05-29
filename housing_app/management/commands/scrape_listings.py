from django.core.management.base import BaseCommand
from housing_app.scraper import (
    fetch_html,
    parse_listings,
    passes_requirements,
    create_listing,
)

class Command(BaseCommand):
    help = "Scrape external real-estate sites and create Listing objects"

    def add_arguments(self, parser):
        parser.add_argument('--url', action='append', help='Target listing URL to scrape')

    def handle(self, *args, **options):
        urls = options.get('url') or []
        if not urls:
            self.stderr.write('No target URLs provided.')
            return

        for url in urls:
            self.stdout.write(f'Scraping {url}...')
            try:
                html = fetch_html(url)
            except Exception as exc:
                self.stderr.write(f'Failed to fetch {url}: {exc}')
                continue

            for data in parse_listings(html):
                if passes_requirements(data):
                    listing, created = create_listing(data)
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Created listing at {listing}"))
                    else:
                        self.stdout.write(f"Listing already exists: {listing}")
        self.stdout.write(self.style.SUCCESS('Scraping complete.'))
