Title: REST API with Django - Part 3
Date: 2024-10-18 00:00 
Modified: 2024-10-18 00:00 
Category: Blog 
Tags: django, drf, openapi, rest, python 
Slug: django-rest-apis-openapi-documentation
Authors: Odolix
Summary: A set of posts on developing a REST API using Django: How to document an API with OpenAPI, SwaggerUI and DRF Spectacular

# Part 3 - Documenting the API

## DRF Spectacular 

[DRF Spectacular](https://drf-spectacular.readthedocs.io/en/latest/readme.html) is a DRF module for documenting APIs using OpenAPI and Redoc documentation. It is an active package and provides the latest OpenAPI specification: OpenAPI 3.2.

### SwaggerUI

SwaggerUI is my prefered format since it provides a complete and interactive OpenAPI documentation. It is extensible and can handle multiple types of authentication protocols. It allows to provide exampla and predefines values, making it easy t setup values for a test environment. In most cases, SwaggerUI is good enough for testing and replaces Postman for simple queries.

### Redoc

I find the Redoc format more compact and easier to read, but the lack of interactivity makes it less interesting for a regular use. 

## DRF integration

DRF Spectacular integration with DRF is straightforward. 
Install the package pip install drf-spectacular
```pip install drf-spectacular```
Add it to your installed apps in settings.py
```
INSTALLED_APPS = [
    ...
    drf_spectacular
    ...
]
```

add the configuration to settings.py

```
REST_FRAMEWORK = {
    ...
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    ...
}

SPECTACULAR_SETTINGS = {
    "TITLE": "My REST API",
    "DESCRIPTION": """
<h1>My set of APIs</h1>

<p>This is what it does.</p>
<p>This API requires authentication.</p>
""",
    "VERSION": "0.0.1",
}
```

and finally add the routes in the urls.py

```
...
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    ...
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Optional UI:
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ...
]
```

This is enough to get started and have DRF Spectacular parse the available viewsets and generate a OpenAPI document. 

![Alt Resulting Swagger content]({static}/images/todo_swagger_simple.png)
Here is a simple version of the swagger interface

![Alt Resulting Redoc content]({static}/images/todo_redoc_simple.png)
And the basic Redoc interface

### Extending the documentation

Now that we have a base documentation running we can extend the documentation.

To add additional information to a view, we need to  decorate it with the extend_schema function from DRF Spectacular. 

Let's check out the todos/viewsets.py file

```
"""Viewsets for TodoModel."""
...
from drf_spectacular.utils import extend_schema
...

class TodoViewSet(viewsets.ModelViewSet):
    ...

    @extend_schema(
        summary=_("List todos"),
        operation_id="List todos",
        description="List all todos",
        responses={200: TodoListSerializer},
        tags=["Todos"]
    )
    def list(self):
        return super().list()
```
![Alt Resulting Swagger for Todos List]({static}/images/todos_swagger_list.png)
Which results in more user friendly info on the view.

- "summary" attribute displays on the line.
- "description" is displayed in the detail.
- "responses" lists posible responses, and feeds the list of schemas at the bottom of the page
- "tags" group routes per tag. Several tags will result in a route appearing on every tag group.

### Decorating without overloading the function

In the previous chapter, the decorator was added on the overloaded ```list``` function. But that is not very practical if you want to document a standard set of routes. 

This will save time and code
```
@extend_schema_view(
    list=extend_schema(description='List all todos')
)
class TodoViewSet(viewsets.ModelViewSet):
    ...
```

### Excluding routes 

If you want to exclude a route from the documentation, you can use the ```exclude``` keyword in ```extend_schema```. 

The route will not appear in the documentation, but it will still be callable! 

### Custom actions

If you want to add custom views to your ViewSet, you can use the ```action``` decorator to declare a specific route. Combined with ```extend_schema```, you can make custom routes easy to understand to your users.

Adding a ```/todos/count/``` route is pretty simple

```
class TodoViewSet(viewsets.ModelViewSet):
    ...

    @extend_schema(
        summary=_("Count todos"),
        operation_id="Count todos",
        description="Count all todos",
        responses={200: TodoCountSerializer},
        tags=["todos"]
    )
    @action(methods=["GET"], detail=False, url_path="count", url_name="count")
    def count(self, request):
        return {"count": TodoModel.objects.count()}
```        

![Alt Todo count]({static}/images/todos_count_action.png)

___Note___ that even for a simple view, I use a Serializer to return the result. It makes maintenance easier by handling the output in a class. You can then inherit that serializer from a parent class that wraps the result in a more complex response. 

### Schema documentation 

When using a serializer as output, DRF Spectacular adds it to the schema dictionnary. 

Fields documentation can come from different places: 
- from the model field lables when the serializer is a ModelSerializer

```
class TodoModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField("Summary of the action to perform", max_length=255)
    description = models.TextField("Long description of what is expected", null=True, blank=True)
    due_date = models.DateField("Optional date for completion", null=True, blank=True)
    assignee = models.ForeignKey(User, verbose_name="User that is expected to do the action", on_delete=models.CASCADE, null=True, blank=True, related_name="assigned_tasks")
    created_by = models.ForeignKey(User, verbose_name="User that created the action", related_name='created_tasks', on_delete=models.CASCADE)
    created_at = models.DateTimeField("Date of creation", auto_now_add=True)
    updated_by = models.ForeignKey(User, verbose_name="User that updated the action", related_name='updated_tasks', on_delete=models.CASCADE)
    updated_at = models.DateTimeField("Date of last modification", null=True, blank=True)
    deleted_by = models.ForeignKey(User, verbose_name="User that deleted the action", related_name='deleted_tasks', on_delete=models.CASCADE)
    deleted_at = models.DateTimeField("Date of deletion", null=True, blank=True)
```

- from the serializer field label

```
class TodoCountSerializer(serializers.Serializer):
    count = serializers.IntegerField(label=_("Number of todo items"), read_only=True)
```

![Alt Todo list schema]({static}/images/todos_schema.png)

### Input parameters documentation 

You can also document input parameters using the ```parameters``` attribute and passing it a list of parameters:
- an OpenApiParameter object

```
OpenApiParameter(
    "ip",
    OpenApiTypes.UUID,
    OpenApiParameter.PATH,
    description=_("Object UUID"),
),
```
- a serializer
```
class TodoModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(help_text="Summary of the action to perform", max_length=255)
    description = models.TextField(help_text="Long description of what is expected", null=True, blank=True)
    ...

class TodoCreateSerializer(serializers.ModelSerializer):
    """Input serializer for Todo creation."""
    name = serializers.CharField(help_text="Name of the action, less than 255 chars")
    description = serializers.CharField(help_text="Long text description")

    class Meta:
        model = TodoModel
        fields = ["name", "description"]

```

![Alt Todo list schema]({static}/images/todo_create_parameters.png)
The help_text attribute on the serializer field or on the model field sets the description of the parameter

## Global configuration

Global configuration happens in the ```SPECTACULAR_SETTINGS``` variable in the ```settings.py``` file.
The following keys can make the Swagger interface more usable.

### SwaggerUI

SwaggerUI provides a set of paramaters to customize the interface without having to override the template.

```
"SWAGGER_UI_SETTINGS": {
    "deepLinking": True,
    "persistAuthorization": True,
    "displayOperationId": True,
    "displayRequestDuration": True,
    "filter": True,
    "tryItOutEnabled": True,
},
```

- "deepLinking" allow to open the Szagger inerface directly on a specific route. It is useful if your documentation is getting long, and our want to build a menu. 
- "persistAuthorization" enables the retention of the authentication parameters when reloading the page. Very useful during development and testing.
- "displayOperationId" can help you identify the correct method used on a route if you have conflicting routes.
- "displayRequestDuration" can help tracking uderperforming routes
- "filter" sets a filter field to search for a specific route. Useful if your documentation is very long
- "tryItOutEnabled" makes the interface interactive and allows you to query the server

### Servers

Defining servers can help with managing different environments with a unique interface.

```
"SERVERS": [
    {
        "url": f"{self.server}" + "/{site}",
        "description": "Todo server",
        "variables": {
            "site": {
                "default": os.environ.get(
                    "DEFAULT_SITE"
                ),
                "description": "Default todo site",
            },
        },
    }
],
```

In that exemple, the Server URL takes a mandatory variable (site) that will appear on the Swagger interface, and that can be set to a default value through environment variables.


### Prefixing

In the previous case, all URLs are in the form of 
```/{site}/todos/```. Not because the servers provides a path element, but because of a prefix in the urls.py configuration. 

But we don't want that because we provide that value through the server URL and we don't want the site to be an input parameter for all routes. 

To avoid that, we can use the SCHEMA_PREFIX key.

```"SCHEMA_PATH_PREFIX": "/{site}",```

This will remove ```/{site}``` from all routes in the documentation, leaving the documentation with only ```todos/``` which makes it more readable and usable.

### Filtering routes

Finally, there might be some routes that you want to filter, so that they don't appear in the schema.

DRF Spectacular offers preprocessing hooks, that can limit the routes available.

Image we have setup a list of ```/internal/todos/

```
def preprocess_exclude_routes(endpoints, **__):
    """
    preprocessing hook that filters out {format} suffixed paths, in case
    format_suffix_patterns is used and {format} path params are unwanted.
    """
    client_id_path = f"{{{settings.CLIENT_ID_VARIABLE}}}"
    return [
        (path, path_regex, method, callback)
        for path, path_regex, method, callback in endpoints
        if client_id_path in path
    ]

PREPROCESSING_HOOKS=[preprocess_exclude_routes]
```


## Wrap up

Documentation is a key to use your API with efficiency and autonomy. DRF Spectacular provides a powerful tool to generate documentation from code.

The code is available [here](https://github.com/fmodolix/todos)
