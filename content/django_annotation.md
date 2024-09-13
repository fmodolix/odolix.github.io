Title: Django Annotate and Manager
Date: 2024-09-12 00:00
Modified: 2024-09-12 00:00
Category: Blog
Tags: django, orm, annotate
Slug: django_annotation
Authors: Odolix
Summary: Beware when mixing annotate and model manager

Django ORM is a powerful beast! 

I started using Django using Django 1.3, and the ease of use of the ORM was the reason I chose and stayed with Django. 

## Annotation

Amongst the many features of Django ORM are the annotation and agregation capabilities.

It allows to compute values based on groups of items.

Considering the following model: 
```
LoggingModel(models.Model):
  timestamp = models.DateTimeField(auto_now_add=True, primary_key=True)
  client_id = models.CharField(max_length=25)
  duration = models.FloatField(default=0.0)
```

### Agregation example
> SELECT COUNT(*) FROM loggingmodel

would translate to 

> LoggingModel.objects.count()

### Annotation example
> SELECT client_id, COUNT(id), MAX(duration), MIN(duration), AVG(DURATION) FROM loggingmodel GROUP BY client ORDER BY client_id

would translate into

> LoggingModel.objects.values('client_id').annotate(cnt=models.Count('pk'), max=models.Max('duration'), min=models.Min('duration')).order_by('client_id')


### Many more

Django ORM also support subqueries, so it is possible to aggregate from the result of subqueries, allowing to create complex database queries without needing to manually build SQL queries.

## Model Manager

A model manager is a structure that manages collections of objects A default manager is associated automatically with a Model class on the 'objects' property. 

When calling ```LoggingModel.objects.all()``` we call the LoggingModel default manager all function.

A manager is very efficient when it comes to filter data by default. This is done through the get_queryset function.

Example: Let's build a Manager that filters logs with duration lower than 200ms. 

```
class Over200Manager(models.Manager):
  '''Manager to filter calls taking less than 200ms.'''
  
  def get_queryset(self):
    qs = super().get_queryset()
    return qs.filter(duration__gt=200)
    
class LoggingModel(models.Model):
  ...
  over_200: Over200Manager()
```

## Manager sorting and Annotation

Now let's mix these features. 

As we've seen before, the manager forges the queryset to fill the model.

It can lead to tricky situations. 

Let's consider this manager: 
```
class SortedManager(models.Mannager):
  '''Manager that sorts result.'''
  
  def get_queryset(self):
    qs = super().get_queryset()
    return qs.order_by('-timestamp')
    
class LoggingModel(models.Model):
  ...
  objects = SortedManager()
```

Considering I have 4 different client_ids in the database and 256 rows, if I try to aggregate on the client_id 

> LoggingModel.objects.values('client_id').annotate(cnt=models.Count('id'))

I'll get 256 rows in the result and not 4 as expected. 

### Sorting and annotation

When I look at the underlying SQL 

> print(LoggingModel.objects.values('client_id').annotate(cnt=models.Count('id')).query)

I get 

> SELECT client_id, COUNT(timestamp) FROM loggingmodel GROUP BY client_id, timestamp ORDER BY timestamp

I did not ask for the timestamp explicitely, but it is in my query. 

This comes from the manager: the get_queryset fonction adds the sorting, and thus introduces the timestamp into the query. 

To avoid this situation, avoid sorting in the queryset, sort as the last resort before evaluating the query. 

