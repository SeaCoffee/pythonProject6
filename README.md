# Python Django Rest Framework

A Django REST Framework (DRF) API with authentication, user management, and post creation.  
Uses Docker for containerization, Simple JWT for authentication, and Celery with Redis for email notifications.  
Dependencies are managed with Poetry.

## How to Run with Docker

1. Build and Start Containers

1. docker compose build                                                  2. docker compose up 


2. Apply Database Migrations

docker-compose run --rm app sh

Inside the container:

python manage.py makemigrations python manage.py migrate


## Testing API with Postman

1. Import the python-drf.postman_collection.json file into Postman.
2. Start the server (docker-compose up).
3. Use real email addresses for testing user registration, as activation links are sent via email.

## Email Activation

- Users must verify their email via a link.
- Ensure SMTP settings are configured for sending emails.

## Useful Commands

Stop Containers:

docker-compose down


View Logs:

docker-compose logs -f app


Create a Superuser:

docker-compose run --rm app sh python manage.py createsuperuser


## Additional Notes

- Ensure .env is properly configured.
- API endpoints are documented in the Postman collection.
- Celery & Redis are used for email notifications.
