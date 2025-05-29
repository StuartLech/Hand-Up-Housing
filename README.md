# Hand-Up-Housing

This project is a Django application for managing housing resources.

## Prerequisites

- **Python 3.11** (the project was developed using Python 3.11)
- **virtualenv** or a similar tool to create an isolated Python environment

## Setup

1. Create and activate a virtual environment:
   ```bash
   rm -rf venv
   python3.12 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Install dependencies:
   ```bash
   pip install --upgrade pip setuptools wheel
   pip install -r requirements.txt
   ```
3. Apply migrations and start the development server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
The application will be available at `http://127.0.0.1:8000/` by default.

## Importing Listings from an API

Volunteers can import property listings from an external API endpoint. Visit
`/scrape/api/` while the server is running and provide the API URL and optional
API key. The response should be a JSON array of listing objects with fields like
`street`, `city`, `state`, `zip`, `bedrooms`, `bathrooms`, `property_type`,
`lease_term`, `hud_subsidy` and `rent`. Listings that meet the Madison County
requirements will be created automatically.

For quick testing the repository includes `static/sample_listings.json` which
contains two example listings. When the Django development server is running
with `DEBUG=True`, this file is available at
`http://127.0.0.1:8000/static/sample_listings.json`. Supplying this URL to
`/scrape/api/` demonstrates the import functionality without relying on an
external service.

## Deployment

Before deploying to production, collect static assets with:

```bash
python manage.py collectstatic
```

The files will be placed in the `staticfiles/` directory.

## Documentation

Additional PDFs are available in the `Documentation/` folder:

- `Hu4h final documentation.pdf`
- `SRS Document.pdf`
- `User Documentation.pdf`

These files contain optional design and user guides.
