# My Django Package

My Django Package is a web application for managing and querying documents using a chatbot interface. It supports multiple file formats, extracts text from documents, and uses an AI model to answer questions based on the content of uploaded documents.

## Features

- Upload and manage documents in various formats (PDF, DOCX, PPTX, TXT, CSV, etc.)
- Extract text from uploaded documents
- Query documents using a chatbot interface
- Provide feedback on responses
- View and manage chat sessions

## Installation

### Prerequisites

- Python 3.11
- Django 3.2 or higher

### Steps

1. Install the package:

```bash
pip install -e .

django-admin startproject myproject
cd myproject


# myproject/settings.py

INSTALLED_APPS = [
    ...
    'app1',
    ...
]


# myproject/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app1.urls')),  # Add this line to include app1's URLs
]


python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

pip install awscli

aws configure   # To Configure aws credentials

python manage.py runserver

Open your browser and navigate to http://127.0.0.1:8000/ to see your Django project with the integrated app1 app.

```
