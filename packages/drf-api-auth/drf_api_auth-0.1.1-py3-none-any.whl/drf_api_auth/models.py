from django.conf import settings
from django.db import models
from django.utils.crypto import get_random_string

from drf_api_auth import settings as drf_api_auth_settings


class ApiAuth(models.Model):
    api_key = models.CharField(max_length=255, db_index=True, unique=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="api_auth", on_delete=models.CASCADE
    )

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = "drf_api_auth" not in settings.INSTALLED_APPS
        verbose_name = "API Auth"
        verbose_name_plural = "API Auths"

    def save(self, *args, **kwargs):
        if not self.api_key:
            self._generate_api_key()
        return super().save(*args, **kwargs)

    @classmethod
    def _get_random_string(cls):
        return get_random_string(drf_api_auth_settings.DRF_API_KEY_LENGTH)

    def _generate_api_key(self):
        self.api_key = self._get_random_string()
