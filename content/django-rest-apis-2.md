Title: REST API with Django - Part 2
Date: 2024-09-11 00:00 
Modified: 2024-09-11 00:00 
Category: Blog 
Tags: django, drf, openapi, rest, python 
Slug: django-rest-apis-project-structure
Authors: Odolix
Summary: Setup a project structure for Django REST project

# REST API with Django

A set of posts on developing a REST API using Django

## Part 2 - Project structure

### Django project and modules - reuse 

Django has a 2 level architecture: 

- a project, that contains settings and that is run
- apps, that contain domain specific code and that are included in a project.

When creating a django project, you can either include apps directly as sub folders, or indirectly as external python packages.

I used to split code into different repos to enhance re-usability of the code, but with monorepo and packaging tools like PDM, it's easier to have a single repo and to deploy modules based on your needs and dependencies. 

### Project structure

A typical project would have this file: manage.py, which is the Django CLI file. It allows to launch management commands like migrations and translations, and launch the dev server. 

Here is a common structure on my projects: 

- manage.py
- config: project configuration folder, specific to the execution environment
    - settings.py: file containing general project settings
    - asgi.py: asgi server parameters, asgi is the asynchronous server
    - wsgi.py: wsgi server parameters, wsgi is the classic server
    - urls.py: project routing, includes module routing
- .gitignore: don't commit cache files or env files
- pyproject.toml: project package settings
- README.md: Explain what your project does
- docker: provide a docker script to run the service

### App structure

An app is a domain code. It contains models, views, and controllers for one domain, and should not mix different domains.

The common app / module structure looks like this: 

- models.py: contains model classes
- viewsets.py: contains REST CRUD controllers
- serializers.py: Serialization classes, used for validation and formatting of information
- tests.py: Unit and functional tests
- urls.py: routing for this app

When building a pure REST service, I don't use django's views.py because I don't serve Views.

I often use these additional files: 

- filters.py: manage django-filters classe to handle query param filtering 
- permissions.py: manage REST permisison classes

### Micro-service / Domain app

When dealing with a microservice, each app will contain a very simple model, along with serializers and viewsest. In that case, the above structure is sufficient.

If I deal with a domain / macro-service REST API, I have to deal with larger models, serializers and viewsets, so I split the files into subfolders:

- models
    - `__init__.py`
    - model1.py
    - ...
- serializers: 
    - `__init__.py`
    - model1_serializers.py
    - ...
 
and so on.

### Wrap up

This is a minimal structure that can be extended, but that covers most of my needs, while keeping things organized and easy to manage and expand.