# LibraryProject

A Django web application for managing a library system.

## Project Overview

This is a Django-based library management system created as part of the ALX Django Learn Lab curriculum. The project serves as an introduction to Django web development and will be expanded to include features for managing books, authors, and library operations.

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/Alx_DjangoLearnLab.git
   cd Alx_DjangoLearnLab/Introduction_to_Django/LibraryProject
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Django:**
   ```bash
   pip install django
   ```

4. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

5. **Access the application:**
   Open your browser and go to `http://127.0.0.1:8000/`

## Project Structure

```
LibraryProject/
├── README.md
├── manage.py
└── LibraryProject/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    └── asgi.py
```

## Key Files

- **`manage.py`**: Command-line utility for Django project management
- **`settings.py`**: Project configuration and settings
- **`urls.py`**: URL routing configuration
- **`wsgi.py`**: WSGI application entry point for deployment
- **`asgi.py`**: ASGI application entry point for async support

## Development Commands

- **Start development server**: `python manage.py runserver`
- **Create database migrations**: `python manage.py makemigrations`
- **Apply migrations**: `python manage.py migrate`
- **Create superuser**: `python manage.py createsuperuser`
- **Create new app**: `python manage.py startapp <app_name>`

## Features (Planned)

- [ ] Book management (CRUD operations)
- [ ] Author management
- [ ] User authentication and authorization
- [ ] Book borrowing system
- [ ] Search and filtering capabilities
- [ ] Admin interface for librarians

## Learning Objectives

Through this project, you will learn:
- Django project structure and organization
- URL routing and view handling
- Model-View-Template (MVT) architecture
- Database integration with Django ORM
- User authentication and permissions
- Template rendering and static file management

## Contributing

This project is part of the ALX Django Learn Lab curriculum. Please follow the course guidelines for contributions and submissions.

## License

This project is created for educational purposes as part of the ALX Software Engineering program.

## Support

For questions or issues related to this project, please refer to the ALX Django Learn Lab documentation or reach out to your instructors.

---

**Created by:** Adeyiwola success
**Date:** July 2025  
**Course:** ALX Django Learn Lab  
**Module:** Introduction to Django