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

The React interface requires no build step and is loaded directly from static
files located in the `static/` directory. During development Django locates
them automatically via the `STATICFILES_DIRS` setting. Before deployment make
sure to collect the files with:
```bash
python manage.py collectstatic
```

The React front end is available at `/react/` while the development server is
running. Access `http://127.0.0.1:8000/react/` in your browser and verify that
the page loads without any 404 errors.

The application will be available at `http://127.0.0.1:8000/` by default.

## Documentation

Additional PDFs are available in the `Documentation/` folder:

- `Hu4h final documentation.pdf`
- `SRS Document.pdf`
- `User Documentation.pdf`

These files contain optional design and user guides.
