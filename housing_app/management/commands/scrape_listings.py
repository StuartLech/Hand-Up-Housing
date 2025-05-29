from django.core.management.base import BaseCommand
from housing_app.scraper import scrape_urls

class Command(BaseCommand):
    help = "Scrape external real-estate sites and create Listing objects"

    def add_arguments(self, parser):
        parser.add_argument('--url', action='append', help='Target listing URL to scrape')

    def handle(self, *args, **options):
        urls = options.get('url') or []
        if not urls:
            self.stderr.write('No target URLs provided.')
            return

        messages = scrape_urls(urls)
        for msg in messages:
            if msg.startswith('Failed'):
                self.stderr.write(msg)
            else:
                self.stdout.write(msg)
