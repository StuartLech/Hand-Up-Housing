# Hand-Up-Housing

This project is a Django application for managing housing resources.

The repository now includes a lightweight React front-end. You can access it by
visiting `/react/` while the Django server is running. The React app uses a
simple JSON API served from the Django backend.

## Prerequisites

- **Python 3.11** (the project was developed using Python 3.11)
- **virtualenv** or a similar tool to create an isolated Python environment

## Setup

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply migrations and start the development server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

The React interface requires no build step and is loaded directly from static
files.

The application will be available at `http://127.0.0.1:8000/` by default.

## Documentation

Additional PDFs are available in the `Documentation/` folder:

- `Hu4h final documentation.pdf`
- `SRS Document.pdf`
- `User Documentation.pdf`

These files contain optional design and user guides.
