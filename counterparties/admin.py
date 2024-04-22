from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Counterparty, Agreement, ContactPerson, Contact


@admin.register(Counterparty)
class CounterpartyAdmin(ImportExportModelAdmin):
    list_display = ('public_id', 'edrpou', 'short_name', 'full_name',
                    'address')


@admin.register(Agreement)
class AgreementAdmin(ImportExportModelAdmin):
    list_display = ('public_id', 'short_name', 'number', 'commencement_date',
                    'expiration_date', 'payment_delay_days', 'total_value',
                    'counterparty', 'type', 'description')


@admin.register(ContactPerson)
class ContactPersonAdmin(ImportExportModelAdmin):
    list_display = ('public_id', 'short_name', 'agreement', 'full_name',
                    'position', 'notes')


@admin.register(Contact)
class ContactAdmin(ImportExportModelAdmin):
    list_display = ('public_id', 'short_name', 'contact_person', 'type',
                    'value', 'notes')

