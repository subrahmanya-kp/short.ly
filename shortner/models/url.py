from django.db import models

from ..snowflake import generate_short_code

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

    def resolve_url(self):
        return self.long_url
