# AI Contribution Guidelines

This project is a Django application for managing housing resources. The repository contains source code, documentation PDFs, static assets, and a Python virtual environment.

## Project Structure
- `housing_app/` - Main Django app with models, views, forms, and templates.
- `housing_site/` - Site configuration and settings module.
- `static/` - Static files served by Django. Includes admin assets and custom JS/CSS.
- `media/` - Uploaded media files (kept empty in version control).
- `Documentation/` - PDF documentation for reference.
- `venv/` - Local virtual environment. Do not modify or commit files here.

## Development Environment
- Use **Python 3.11 or newer**. The README uses Python 3.12 to create the virtual environment.
- Install dependencies with `pip install -r requirements.txt`.
- The project does not include automated tests. To perform a basic check, run:
  ```bash
  python -m py_compile $(git ls-files '*.py' | grep -v '^venv/')
  ```
- You can also run `python manage.py check` to validate the Django configuration.

## Style Guidelines
- Format Python code using **black** with default settings: `black .`.
- Follow PEP8 for naming and imports. Use 4 spaces per indentation level.
- Keep lines under **88 characters** when possible (black's default).

## Pull Request Checklist
1. Ensure new Python files compile without errors using the command above.
2. Run `black .` before committing changes.
3. Include clear commit messages describing the purpose of the change.
4. Mention any manual steps or limitations in the PR body.

## Notes for AI Agents
- Avoid modifying the virtual environment (`venv/`).
- When adding images or static files, place them under `static/` with meaningful names.
- Additional folder-specific guidelines are provided in nested `AGENTS.md` files.
- Avoid committing changes to `db.sqlite3` unless specifically required for sample data.
