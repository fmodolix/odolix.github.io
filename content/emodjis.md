Title: Building a front end with Django-Unicorn
Date: 2024-09-13 00:00 
Modified: 2024-09-13 00:00 
Category: Blog
Tags: python, django, web, livewire, unicorn, front end, livewire, hotwire
Slug: emoticons-django-unicorn
Authors: Odolix 
Summary: Building a front end to the emoticon service using the Livewire like Django-Unicorn library

# Building a front end

## Django-Unicorn, Hotwire, Livewire

[Django-Unicorn](https://www.django-unicorn.com/) is a young but promising extension to Django to handle dynamic front ends using Django's template rendering. 
It follows the concepts developped on Livewire - "Building modern Web Apps is hard" - and ports it to Django. 
These concepts gained traction when they were implemented by 37signals on their Hey.com new e-mail platform using RoR.

## front end development

Building a new front end with a front end framework is a long process: 

- Build a data model
- Build a presentation layout
- Style the components
- Add behaviour
- Authenticate with the back end
- Fetch and map back end data with the front end

Building a template is a bit more straight forward:

- Build a presentation layout
- Style the component
- Add behaviour

But building a front end with templates gives limited interaction with the user, and requires page loading to change the context.

If I had to weigh the different phases as a mostly back end developer, I'd put:
 
- Build a data model: small
- Building a presentation layout: medium
- Style the components: large (devil's in the detail)
- Add behaviour: medium
- Authenticate with the back end: large, OIDC has a lot of requirements
- Fetch and map data: small

When developing a small site that is a very heavy, especially the auth part.

# The project

## Presentation

The project is quite simple, I switched from Slack to Teams for different reasons, and I wanted to keep using the emoticons that I had in Slack. 
I stumbled upon that project : [custom-emoji-server](https://github.com/dsmiller95/custom-emoji-server) but wasn't able to make it work. 


Considering the effort to debug the problem and the depth of the lib, I decided to build my own using Django, which I am more proficient with. 

## The back end

The code is available [here](https://github.com/fmeurou/emodjis). 

The model is pretty simple: 

```
class Emoji(models.Model):
    ...
    name = models.CharField(max_length=255, primary_key=True)
    uses = models.IntegerField(default=0)
    image = models.BinaryField(null=True)
    team = models.ForeignKey(
        Group,
        related_name="emojis",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    nsfw = models.BooleanField(default=False)
    private = models.BooleanField(default=False)
```
 
name and image are the basic fields, and some additional filtering properties to manage private and NSFW icons.

I build a basic REST API using Django Rest Framework and DRF-Spectacular for documentation: 

![Alt Resulting Swagger content]({static}/images/emojis_swagger.png)

## The front end

At first, I did not care about the front end, it was supposed to integrate with Teams (that part is still very uncertain :D).

But it was a good opportunity to do a front end POC. 

![Alt Resulting fronted]({static}/images/emojis_front end.png)

As you can see, the front end is quite bare: a list of images with search and pagination. But I did not want to reload the page every time I filter or paginate, and I did not want to build a React or Vue site.

### Layout and styling

To speed up the layout and styling (it's a POC interface), I use Boostrap and Tailwind. 
Bootstrap is a straightforward and popular component library that will handle the layout, and Tailwind handle the styling and positioning. 

I use the [django-bootstrap5](https://github.com/zostera/django-bootstrap5) package to inject bootstrap in my templates.

The templates/base.html page reflects that:

```
{% extends 'bootstrap.html' %}
{% load django_bootstrap5 %}
{% load unicorn %}
{% block bootstrap5_extra_head %}
    <script src="https://cdn.tailwindcss.com"></script>
    {% unicorn_scripts %}
{% endblock %}

{% block bootstrap5_content %}
    {% csrf_token %}
    <div class="container">
        <div name="header" class="container mx-auto bg-green-500 rounded place-content-center p-2 m-2">
        <span class="text-2xl text-uppercase">{% block content_title %}(no title){% endblock %}</span>
        </div>

        {% autoescape off %}{% bootstrap_messages %}{% endautoescape %}
        <div name="content"  class="container mx-auto p-2 m-2">
        {% block content %}(no content){% endblock %}
        </div>
    </div>

{% endblock %}
```

### Including Unicorn

To include unicorn into the site, I simply load the unicorn template tag into the main page:

```
{% extends "base.html" %}
{% load django_bootstrap5 %}
{% load unicorn %}

{% block title %}{{ title }}{% endblock %}
{% block content_title %}<a href="/" class="tracking-wide text-white text-center"><b>{{ title }}</b></a>{% endblock %}

{% block content %}
    {% csrf_token %}
    {% unicorn 'emoji-grid' id='emoji-grid' key='emoji-grid' %}
{% endblock %}
```

## Components

Unicorn works with components, like Vue or React. It makes the development well structured and eases the re-use. 

A component is composed of a UnicornView class and a related template. The class passes its attributes to the template, and modifications to an attribute are updated on the model through a binding mechanism. 

Here is the structure of the app with unicorn components: 

- emodjis <- App folder
    - components <- Where the component classes live
        - emoji_grid.py <- emoji_grid component code
    - ... <- app classes
    - templates
       - unicorn
           - emoji-grid.html <- template for the emoji-grid component
       - index.html <- Full page source
       

### Include components

To include components in a page, use the `{% load unicorn %}`tag in the page. 

Here is the code for the index.html page 

```
{% extends "base.html" %}
{% load django_bootstrap5 %}
{% load unicorn %}

{% block title %}{{ title }}{% endblock %}
{% block content_title %}<a href="/" class="tracking-wide text-white text-center"><b>{{ title }}</b></a>{% endblock %}

{% block content %}
    {% csrf_token %}
    {% unicorn 'emoji-grid' id='emoji-grid' key='emoji-grid' %}
{% endblock %}
```

First we include unicorn in the page, then we load components: ```{% unicorn 'emoji-grid' id='emoji-grid' key='emoji-grid' %}```. 

`id` and `key` are necessary if you use component hierarchy. 

### Component hierarchy

In this project, I wanted the emoticon list to be searchable and paginated. 

At first, I put everything in the same component. It is easier, but it make the component less reusable. e.g.: I want to use pagination over and under the list, and I did not want to duplicate the code. After all, that's what components are for.

So I split the code into 3 components:

- emoji_grid: the list itself
- search: the search button
- pagination: the pagination component

#### front end

The emoji_grid.html template looks like that:

```
{%load i18n  %}
{% load unicorn %}
<div>
    <div class="flex place-content-right">{% unicorn 'login' id='login' key='login' %}</div>
    <div class="flex place-content-center">{% unicorn 'search' id='search' key='search' %}</div>

    <div name="grid" id="emojis_grid" class="container m2 p-2">
        {% for emoji in emodjis %}
            <div class="card d-inline-block" style="width: 3rem;" id="img_{{ emoji.name }}">
                <img class="card-img-top transition ease-in-out hover:-z-[100] hover:scale-[1.5] active:scale-[2.0] p-1" src="data:image/gif;base64,{{ emoji.b64image }}" alt="{{ emoji.name }}"
                     onclick="navigator.clipboard.writeText('{{ emoji.url }}');"
                     title="{{ emoji.name }}">
            </div>
        {% endfor %}
    <div class="container"><p class="">Click on icon to copy to clipboard</p></div>
    </div>
    <div class="container bg-gray-200">{%  unicorn 'pagination' id='bottom_pagination' key='bottom_pagination' %}</div>
</div>
```

It's pretty small and easy to understand: 

- search bar
- content of the grid
- pagination (yes, just one...)

The child components are included in the component as the main component is included in the main page: using the **unicorn** tag. 

Both sub-components have a **key** and an **id**,  otherwise the javascript cannot find them during update. 

#### back end

The back end is also quite straigtforward: 

```
# grid.py
from django_unicorn.components import UnicornView
from django.core.paginator import Paginator
from ..models import Emoji
from ..serializers import EmojiSerializer

PAGE_SIZE = 100


class EmojiGridView(UnicornView):
    name_search = ""
    emodjis = None
    page_range = 0
    page = 1

    def mount(self):
        self.load_emojis()

    def load_emojis(self, search="", page=1, nsfw=False, private=False):
        self.name_search = search
        if not self.request.user.is_authenticated:
            emodjis = Emoji.objects.filter(nsfw=False)
        else:
            if nsfw:
                emodjis = Emoji.objects.nsfw(user=self.request.user)
            else:
                emodjis = Emoji.objects.sfw(user=self.request.user)
        if not private:
            emodjis = emodjis.filter(private=False)
        if search:
            emodjis = emodjis.filter(name__icontains=search).order_by("name")
        else:
            emodjis = emodjis.filter(
                name__icontains=self.name_search
            ).order_by("name")
        p = Paginator(emodjis, PAGE_SIZE)
        self.page_range = list(p.page_range)
        self.page = page
        self.emodjis = EmojiSerializer(
            p.page(page).object_list,
            many=True,
            context={"request": self.request},
        ).data

    def get_page_range(self):
        return self.page_range
```


A class with page and search attributes, and a load_emojis function that applies the logic to fetch and paginate the content. 

This method is called on mount, so when the component is created to hydrate it. 

The linking between the parent and its children is declared in the child: 

```
# emodjis/components/pagination.py
from django_unicorn.components import UnicornView


class PaginationView(UnicornView):
    page = 1
    page_range = None

    def hydrate(self, *args, **kwargs):
        self.page_range = self.parent.get_page_range()
        self.page = self.parent.page

    def updated_page(self, query=1):
        self.page = query
        self.parent.load_emojis(page=query)
        self.page_range = self.parent.get_page_range()
        self.parent.force_render = True
```

the **hydrate** and **update_page** both reference the parent. 

**hydrate** is called when the component is mounted and before data is loaded. In this example, we get the page range and the current page from the parent, because the parent is doing all the fetching and pagination, so it knows how many pages there are, and what is the current page. 

**updated_page** is called whenever the front end updates the page value. In our example, that is when the user clicks on a page number in the pagination bar. 
When the page is updated on the front end, the component's **page** attribute is updated and the **load_emojis** function of the parent component is called. Then we force the list to re-render. 

#### authentication

We also use an authentication component to log the user in and reload the list. 

This is a quick and dirty way of handling authentication, the component should rather be in the main page, but that would then require to call the sibling component to refresh, and I did not take the time to look into that approach.

## Wrap it up

It took me about 2 hours to build the back end, and a day to build the front end. That is a small and satisfying project!

### Quirks

Django-Unicorn, is still quite fresh. I thing the implementation is more structured than other implementations I had used so far. 

But during the dev, I stumbled across a problem with child components. Happily it was fixed on release 0.58 the next day. But I have sometimes the list won't reload, not the first time, but the second, or after a while. 

### Conclusion

So, although I would not recommend to use it on a production environment, I really believe this will be a great solution to build interactive web sites for small teams. 

