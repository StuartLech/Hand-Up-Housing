# housing_app Guidelines

This directory contains the primary Django application code.

## Key Files
- `models.py` defines database models for listings and related choices.
- `views.py` handles request/response logic for listing management and scraping.
- `forms.py` contains Django forms used in templates.
- `scraper.py` provides helper functions to import listings from external sources.

## Contributing
- Keep functions small and focused.
- Stick with function-based views to match current style.
- When updating models, generate migrations with `python manage.py makemigrations` and commit them.
- Templates live in `templates/` and use standard Django templating.
  When creating a new page reached via a redirect, include a Back link or
  button that returns to the previous view (usually the listing list) so users
  can easily navigate.

## Testing
- Run `python -m py_compile $(git ls-files 'housing_app/**/*.py')` before committing.
- `python manage.py check` can help identify configuration issues.
