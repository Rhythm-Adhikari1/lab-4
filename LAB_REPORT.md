# LAB REPORT

## 1. Title
SmartCanteen: Django Web Application Demonstrating Core Web Concepts

## 2. Brief Description of Project
SmartCanteen is a simple and unique campus canteen ordering web app built with Django.
It demonstrates:
- handling HTTP requests and different response types
- form data processing and session usage
- URL routing, custom middleware, and templating
- relational database design with ORM and CRUD
- NoSQL-like document storage using JSONField
- authentication and authorization with cookies/sessions
- middleware-based logging, error handling, and security headers

## 3. Objectives
- Understand Django request-response cycle.
- Implement full form handling workflow.
- Use sessions for user-specific state.
- Build URL routing and template-based UI.
- Compare relational modeling and document-style storage.
- Implement authentication and role-based authorization.
- Add production-minded middleware concerns.

## 4. Technology Stack
- Python 3.13
- Django 6.0.3
- SQLite (default relational database)

## 5. MVC/MVT Architecture of the Project
Django uses MVT (Model-View-Template):
- Model: database schema and business logic (`core/models.py`).
- View: request handling and response generation (`core/views.py`).
- Template: frontend presentation (`templates/`).
- URL Dispatcher (Controller-like routing role): maps paths to views (`core/urls.py`, `smartcanteen/urls.py`).

Flow:
1. Browser sends request.
2. URL dispatcher selects view.
3. View reads/writes models using ORM.
4. View returns template response, JsonResponse, or HttpResponse.
5. Middleware runs before and after view for logging/security/error handling.

## 7. Mapping to Required Concepts
- Handling Requests & Responses: `dashboard`, `about_response_demo`, `api_health`.
- Form Data Handling & Sessions: registration, order form, feedback form, visit counter, theme session.
- Routing, Middleware, Templating: app URLs + custom middleware + Django templates.
- Database Integration (Relational vs NoSQL), CRUD, ORM:
  - Relational: Category, MenuItem, Order, OrderItem.
  - NoSQL-like: FeedbackDocument.payload (JSONField).
  - CRUD: MenuItem create/read/update/delete endpoints.
  - ORM: `filter`, `count`, `aggregate`, `select_related`, `prefetch_related`.
- Authentication & Authorization (Cookies/Sessions): Django login/logout/register + `@login_required` + staff-only CRUD.
- Middleware for Logging, Error Handling, Security: `RequestLogMiddleware`, `GlobalExceptionMiddleware`, `SecurityHeadersMiddleware`.

## 8. How to Run
```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open `http://127.0.0.1:8000/`

## 9. Conclusion
The SmartCanteen project successfully demonstrates all requested Django concepts in a simple, unique, and modular structure suitable for academic lab submission.
