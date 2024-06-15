from rest_framework import serializers
from .models import Warehouse, Category, Uom, Good, GoodTransaction, StockCard, \
    Document, DocumentLine


class WarehouseSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')

    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'type', 'active', 'address']


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    parent = serializers.UUIDField(source='parent.public_id', read_only=True,
                                   format='hex')

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']


class UomSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')

    class Meta:
        model = Uom
        fields = ['id', 'short_name', 'full_name']


class GoodSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    category = serializers.UUIDField(source='category.public_id', read_only=True,
                                     format='hex')
    basic_uom = serializers.UUIDField(source='basic_uom.public_id',
                                      read_only=True, format='hex')

    class Meta:
        model = Good
        fields = ['id', 'outer_id', 'uktzed', 'basic_uom', 'vat_rate',
                  'short_name', 'full_name', 'category', 'active']


class StockCardSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    good = serializers.UUIDField(source='good.public_id', read_only=True,
                                 format='hex')
    warehouse = serializers.UUIDField(source='warehouse.public_id',
                                      read_only=True, format='hex')

    class Meta:
        model = StockCard
        fields = ['id', 'good', 'warehouse', 'balance']


class GoodTransactionSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    good = serializers.UUIDField(source='good.public_id', read_only=True,
                                 format='hex')
    card = serializers.UUIDField(source='card.public_id', read_only=True,
                                 format='hex')
    document = serializers.UUIDField(source='document.public_id', read_only=True,
                                     format='hex')

    class Meta:
        model = GoodTransaction
        fields = ['id', 'good', 'card', 'time', 'document', 'transaction_type',
                  'quantity', 'cost']


class DocumentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    counterparty = serializers.UUIDField(source='counterparty.public_id',
                                         read_only=True, format='hex')
    agreement = serializers.UUIDField(source='agreement.public_id',
                                      read_only=True, format='hex')

    class Meta:
        model = Document
        fields = ['id', 'counterparty', 'agreement',  'type', 'time', 'number']


class DocumentLineSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    good = serializers.UUIDField(source='good.public_id', read_only=True,
                                 format='hex')
    document = serializers.UUIDField(source='document.public_id', read_only=True,
                                     format='hex')

    class Meta:
        model = DocumentLine
        fields = ['id', 'good', 'document', 'quantity', 'price', 'vat_rate']