from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Warehouse, Category, Uom, Good, StockCard, GoodTransaction,\
    Document, DocumentLine


@admin.register(Warehouse)
class WarehouseAdmin(ImportExportModelAdmin):
    list_display = ('public_id', 'name', 'type', 'active', 'address')


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ('public_id', 'name', 'parent')


@admin.register(Uom)
class UomAdmin(ImportExportModelAdmin):
    list_display = ('public_id', 'short_name', 'full_name')


@admin.register(Good)
class GoodAdmin(ImportExportModelAdmin):
    list_display = ('public_id', 'short_name', 'full_name', 'outer_id',
                    'uktzed', 'basic_uom', 'vat_rate', 'category', 'active')


@admin.register(StockCard)
class StockCardAdmin(ImportExportModelAdmin):
    list_display = ('public_id', 'good', 'warehouse', 'balance', 'cost')


@admin.register(GoodTransaction)
class GoodTransactionAdmin(ImportExportModelAdmin):
    list_display = ('public_id', 'good', 'card', 'time', 'document',
                    'transaction_type', 'quantity', 'cost')


@admin.register(Document)
class DocumentAdmin(ImportExportModelAdmin):
    list_display = ('id', 'counterparty', 'agreement', 'time', 'number', 'posted')


@admin.register(DocumentLine)
class DocumentLineAdmin(ImportExportModelAdmin):
    list_display = ('public_id', 'document', 'good', 'quantity',  'price',
                    'vat_rate')
