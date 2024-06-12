# Django REST Framework API Auth

Django REST Framework API Auth is a secure API Key and Secret authentication plugin for REST API built with [Django Rest Framework](https://www.django-rest-framework.org/).

<div>
  <a href="https://badge.fury.io/py/drf-api-ath">
      <img src="https://badge.fury.io/py/drf-api-ath.svg" alt="Version"/>
  </a>
</div>

## Quickstart

1 - Install with `pip`:

```bash
pip install drf-api-ath
```

2 - Register the app in the `INSTALLED_APPS` in the `settings.py` file:

```python
# settings.py

INSTALLED_APPS = [
  # ...
  "rest_framework",
  "drf_api_auth",
]
```

4 - Run migrations:

```bash
python manage.py migrate
```

In your view then, you can add the authentication class.

> ⚠️ **Important Note**: By default, authentication is performed using the `AUTH_USER_MODEL` specified in the settings.py file.

```python
from rest_framework import viewsets

from drf_api_auth.authentications import ApikeyAuthentication
from rest_framework.response import Response


class TestViewSets(viewsets.ViewSet):
  authentication_classes = (ApikeyAuthentication,)

  def list(self, request):
    return Response([{"message": "Ok"}], 200)
```

### TODO

- [ ] Prevent save api_key as clear text
- [ ] Toggling (show/hide) for api_key admin field