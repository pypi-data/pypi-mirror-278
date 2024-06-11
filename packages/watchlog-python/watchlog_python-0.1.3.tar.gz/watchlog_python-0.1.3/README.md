# watchlog-python

A Python client for [watchlog](https://watchlog.org/) server.

## Installation

To install the package, use pip:

```bash
pip install watchlog-python
```

# Usage
## 1. Import the Watchlog Class
First, import the Watchlog class from the watchlog package.


```python

from watchlog import Watchlog

```

## 2. Create an Instance of Watchlog
# Create an instance of the Watchlog class.

```python

watchlog_instance = Watchlog()

```


## 3. Using Watchlog in Your Application
# You can use the watchlog_instance to log different types of metrics. Below are examples of how to use various methods provided by the Watchlog class.

```python

# Increment the specified metric by the given value (default is 1)
watchlog_instance.increment('page_views', 10)

# Decrement the specified metric by the given value (default is 1)
watchlog_instance.decrement('items_in_cart', 2)


# Set the specified metric to the given value
watchlog_instance.gauge('current_temperature', 22.5)

# Set the specified metric to a percentage value (0 to 100)
watchlog_instance.percentage('completion_rate', 85)


# Log a system byte metric
watchlog_instance.systembyte('memory_usage', 1024)


```

## 1. Example Usage in a Django View

```python

# views.py
from django.http import HttpResponse
from watchlog import Watchlog

# Create an instance of Watchlog
watchlog_instance = Watchlog()

def some_view(request):
    # Increment the metric without blocking the main thread
    watchlog_instance.increment('view_hits')

    return HttpResponse("This is a view that increments a metric.")
    

```
