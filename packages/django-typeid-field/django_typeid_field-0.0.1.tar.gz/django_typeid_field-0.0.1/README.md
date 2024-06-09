# Django TypeID Field

TypeID is a type-safe extension of UUIDv7, encoding UUIDs in base32 and adding a type prefix. This package provides a field to use in models. For more details about TypeID, visit the [TypeID GitHub repository](https://github.com/jetify-com/typeid).

## Installation

Install it from PyPI:

```sh
pip install django-typeid-field
```


## Usage

First, add it to your applications (Not Required)

```python
INSTALLED_APPS = [
    # ...
    'typeid_field',
    # ...
]
```

You can now use it in your models like:

```python
from django.db import models
from typeid_field import TypeidField

class Profile(models.Model):
    hash = TypeidField(prefix='profile')
```


## TypeidField

This model field is based on `CharField`. All of it's parameters can be used.

Additionally following fields affects outcome of TypeID:


### `prefix` Parameter (Optional)
Specifies the type prefix for the generated TypeID, which impacts the length of the ID and the field in the database. The prefix can be up to 63 characters long, must contain only lowercase alphabetic ASCII characters or underscores, and cannot start or end with an underscore. If the prefix is empty, no separator is used.


## Using TypeidField as `primary_key`
To use TypeID as default `primary_key` you need to explicitly define it in your
model:

```python
from django.contrib.auth.models import AbstractUser
from django.db import models


class SomeModel(models.Model):
    id = TypeidField(primary_key=True, editable=False) # 2x4y6z8a0b1c2d3e4f5g6h7j8k
    # ...

class CustomUser(AbstractUser):
    id = TypeidField(primary_key=True, editable=False, prefix='user') # user_2x4y6z8a0b1c2d3e4f5g6h7j8k
    # ...
```


## Credits
This package is based on [django-nanoid-field](https://github.com/goztrk/django-nanoid-field).
