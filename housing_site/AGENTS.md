# housing_site Guidelines

Configuration for the Django project lives here.

- `settings.py` holds environment settings. Avoid committing sensitive values.
- `urls.py` defines top-level URL patterns and includes `housing_app.urls`.
- `wsgi.py` and `asgi.py` provide entry points for deployment.

When updating settings, keep `DEBUG=True` only for local development. In production set `DEBUG=False` and specify `ALLOWED_HOSTS`.
