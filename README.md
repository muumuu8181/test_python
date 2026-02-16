# Corporate CMS

A production-ready Corporate Content Management System built with Django.

## Features

- **Core Pages:** Manage static pages (About, Services, etc.) with a Rich Text Editor.
- **News/Blog:** Post company news with images, categories, and tags.
- **Contact Form:** Secure contact form with admin notification (messages saved to DB).
- **Admin Interface:** Fully customized admin dashboard for easy content management.
- **Responsive Design:** Built with Bootstrap 5.

## Tech Stack

- Python 3.12+
- Django 4.2+
- SQLite (Development) / PostgreSQL (Production ready)
- Bootstrap 5
- Django Summernote (WYSIWYG Editor)

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run Migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a Superuser:**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the Server:**
    ```bash
    python manage.py runserver
    ```
    Or use the helper script:
    ```bash
    ./run.sh
    ```

## Usage

1.  Access the Admin Panel at `http://127.0.0.1:8000/admin/`.
2.  Login with your superuser credentials.
3.  Create Pages and News Posts.
4.  View the site at `http://127.0.0.1:8000/`.

## Production Deployment Notes

- Set `DEBUG = False` in `config/settings.py`.
- Configure `ALLOWED_HOSTS`.
- Use a production database like PostgreSQL.
- Serve static files using Nginx/Apache.
- Use Gunicorn as the WSGI server.
