from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.utils import timezone

from ..snowflake import generate_short_code


def url_cache_key(short_code: str) -> str:
    return f"url:short_code:{short_code}"


class URL(models.Model):
    long_url = models.URLField(unique=True, max_length=2048)
    short_code = models.CharField(max_length=10, unique=True, db_index=True)
    expiry = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = generate_short_code()
        super().save(*args, **kwargs)
        cache.delete(url_cache_key(self.short_code))

    def resolve_url(self):
        return self.long_url

    def cache_long_url(self):
        ttl = settings.URL_CACHE_TTL_SECONDS
        if self.expiry:
            seconds_to_expiry = (self.expiry - timezone.now()).total_seconds()
            if seconds_to_expiry <= 0:
                return
            ttl = min(ttl, int(seconds_to_expiry))
        cache.set(url_cache_key(self.short_code), self.long_url, timeout=ttl)
