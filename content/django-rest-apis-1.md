Title: Introduction to building a REST API with Django 
Date: 2024-09-10 00:00 
Modified: 2023-09-10 00:00 
Category: Blog 
Tags: django, drf, openapi, rest, python 
Slug: django-rest-apis 
Authors: Odolix
Summary: A tour of the libraries used to bootstrao a django REST API

# REST API with Django

A set of posts on developping a REST API using Django

## Part 1 - Libraries

### My take on Django 

Django is a Web framework in Python. My take on it is that it provides a lot of features, the documentation is easy to read, and there are quite a few examples on the net. 

It probably lacks flexibility due to being a "monolythic" framework, but the behaviour is quite flexible, and can easily be overridden. 
Working with it for more than 10 years, I rarely had to torture it to the point that it goes against the standard behaviour. 

### Django and REST API

Django comes with a lot of features, but it lacks a simple CRUD REST API management. You can hack it with views, but there is an easier way.

Django REST Framework comes in handy when developping APIs. 

It provides data authentication, bermissions, routing, caching, validation, serialization, and all those features you'll need to develop a prefessional API service. 

Take a look at the documentation to have a better idea of its capabilities [1] 

I've used it in conjonction with the Django Models, which is the most common case, but also as a API proxy for other services, using validation and mapping through serialization. 

### REST API and documentation

APIs are useless if not documented. The whole point of an API is to extend your app by allowing communication with other systems. And communication means documentation. 

There are different documentation formats for REST APIs, but the most common is the OpenAPI [2] format, and it's famous Swagger interface. 

Swagger UI [3] enables testing your APIs directly from the Web page, without needing additional tools. At least it's fine for basic testing: you'll probably want to use a tool like Postman [4] in case you want to manage credentials and a context. 

A OpenAPI specification is basically a JSON file, so you could create it manually. But that would be painful and hard to maintain. 

That's where drf-spectacular [5] jumps in. It has OpenAPI 3.0 specification support, handles authentication, and generates documentation from views and class decorators in the code. It can also be configured to setup variables, and to skip part of the path in the documentation. 

### CORS Management

CORS management is fundamental in building APIs, so you'd better install django-cors-headers [6] to make sure other frontends can use your service. 

### Debugging 

Using swagger is pretty much how I test my APIs, on top of building unit tests. However, installing django extensions [7] can come very handy to manage simple tasks like showing available URLs on cleaning the database.

### Wrap up

This is an introduction to the libraries that I generally use to build a REST API backend. There are more libs that can be used, but this is the bare minimum in my opinion to start a new project.


### References


[1] [Django Rest Framework](https://www.django-rest-framework.org/)

[2] [Open API](https://www.openapis.org/)

[3] [SwaggerUI](https://swagger.io/tools/swagger-ui/)

[4] [Postman](https://www.postman.com/)

[5] [DRF-spectacular](https://drf-spectacular.readthedocs.io/en/latest/readme.html)

[6] [Django CORS headers](https://github.com/adamchainz/django-cors-headers)

[7] [Django extensions](https://github.com/django-extensions/django-extensions)
