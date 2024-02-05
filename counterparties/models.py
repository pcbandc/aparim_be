from django.db import models
import uuid


class Counterparty(models.Model):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4)
    edrpou = models.CharField(unique=True, max_length=10)
    short_name = models.CharField(max_length=100, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.short_name} ({self.edrpou})'
