from django.contrib import admin
from .models import Counterparty


@admin.register(Counterparty)
class CounterpartyAdmin(admin.ModelAdmin):
    list_display = ('public_id', 'edrpou', 'short_name',
                    'full_name', 'address')

