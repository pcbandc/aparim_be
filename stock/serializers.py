from rest_framework import serializers
from .models import Warehouse, Category, Uom, Good, GoodTransaction, StockCard, \
    Document, DocumentLine


class WarehouseSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    shortName = serializers.CharField(source='name')

    class Meta:
        model = Warehouse
        fields = ['id', 'shortName', 'type', 'active', 'address']


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    shortName = serializers.CharField(source="name")
    parent = serializers.CharField(source='parent.name', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'shortName', 'parent']


class UomSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    shortName = serializers.CharField(source='short_name')
    fullName = serializers.CharField(source='full_name')

    class Meta:
        model = Uom
        fields = ['id', 'shortName', 'fullName']


class GoodSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id',
                               read_only=True,
                               format='hex')
    shortName = serializers.CharField(source='short_name')
    category = serializers.CharField(source='category.name',
                                     read_only=True)
    category_id = serializers.UUIDField(source='category.public_id',
                                        read_only=True,
                                        format='hex')
    basic_uom = serializers.CharField(source='basic_uom.short_name',
                                      read_only=True)
    basic_uom_id = serializers.UUIDField(source='basic_uom.public_id',
                                         read_only=True,
                                         format='hex')

    class Meta:
        model = Good
        fields = ['id', 'outer_id', 'uktzed', 'basic_uom', 'basic_uom_id',
                  'vat_rate', 'shortName', 'full_name', 'category',
                  'category_id', 'active']


class StockReportSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id',
                               read_only=True,
                               format='hex')
    shortName = serializers.CharField(source='short_name')
    category = serializers.CharField(source='category.name',
                                     read_only=True)
    category_id = serializers.UUIDField(source='category.public_id',
                                        read_only=True,
                                        format='hex')
    basic_uom = serializers.CharField(source='basic_uom.short_name',
                                      read_only=True)
    basic_uom_id = serializers.UUIDField(source='basic_uom.public_id',
                                         read_only=True,
                                         format='hex')
    inflow_total_count = serializers.DecimalField(max_digits=12, decimal_places=3)
    inflow_total_sum = serializers.DecimalField(max_digits=12, decimal_places=2)
    outflow_total_count = serializers.DecimalField(max_digits=12, decimal_places=3)
    outflow_total_sum = serializers.DecimalField(max_digits=12, decimal_places=2)
    start_balance_count = serializers.DecimalField(max_digits=12, decimal_places=3)
    start_balance_sum = serializers.DecimalField(max_digits=12, decimal_places=2)
    end_balance_count = serializers.DecimalField(max_digits=12, decimal_places=3)
    end_balance_sum = serializers.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        model = Good
        fields = ['id', 'outer_id', 'uktzed', 'basic_uom', 'basic_uom_id',
                  'vat_rate', 'shortName', 'full_name', 'category',
                  'category_id', 'active', 'start_balance_count',
                  'start_balance_sum', 'inflow_total_count', 'inflow_total_sum',
                  'outflow_total_count', 'outflow_total_sum',
                  'end_balance_count', 'end_balance_sum']


class StockCardSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    good = serializers.UUIDField(source='good.public_id', read_only=True,
                                 format='hex')
    warehouse = serializers.UUIDField(source='warehouse.public_id',
                                      read_only=True, format='hex')

    class Meta:
        model = StockCard
        fields = ['id', 'time', 'good', 'warehouse', 'balance', 'cost']


class GoodTransactionSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    good = serializers.UUIDField(source='good.public_id', read_only=True,
                                 format='hex')
    card = serializers.UUIDField(source='card.public_id', read_only=True,
                                 format='hex')
    document = serializers.UUIDField(source='document.public_id', read_only=True,
                                     format='hex')
    document_line = serializers.UUIDField(source='document_line.public_id',
                                          read_only=True, format='hex')

    class Meta:
        model = GoodTransaction
        fields = ['id', 'good', 'card', 'document', 'document_line',
                  'transaction_type', 'quantity', 'cost']


class DocumentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    counterparty = serializers.CharField(source='counterparty.short_name',
                                         read_only=True)
    counterparty_id = serializers.UUIDField(source='counterparty.public_id',
                                            read_only=True, format='hex')
    agreement = serializers.CharField(source='agreement.short_name',
                                      read_only=True)
    agreement_id = serializers.UUIDField(source='agreement.public_id',
                                         read_only=True, format='hex')
    posted = serializers.BooleanField(read_only=True, default=True)

    class Meta:
        model = Document
        fields = ['id', 'counterparty', 'counterparty_id', 'agreement',
                  'agreement_id', 'type', 'time', 'number', 'posted']


class DocumentLineSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id',
                               read_only=True,
                               format='hex')
    good = serializers.CharField(source='good.short_name',
                                 read_only=True)
    good_id = serializers.UUIDField(source='good.public_id',
                                    read_only=True,
                                    format='hex')
    warehouse = serializers.CharField(source='warehouse.name',
                                      read_only=True)
    warehouse_id = serializers.UUIDField(source='warehouse.public_id',
                                         read_only=True,
                                         format='hex')
    document = serializers.UUIDField(source='document.public_id',
                                        read_only=True,
                                        format='hex')

    class Meta:
        model = DocumentLine
        fields = ['id', 'good', 'good_id', 'warehouse', 'warehouse_id',
                  'document', 'quantity', 'price', 'vat_rate']