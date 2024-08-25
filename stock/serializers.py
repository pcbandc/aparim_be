from rest_framework import serializers
from .models import Warehouse, Category, Uom, Good, GoodTransaction, StockCard, \
    Document, DocumentLine


class WarehouseSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    shortName = serializers.CharField(source='name')

    class Meta:
        model = Warehouse
        fields = ['id', 'shortName', 'type', 'active', 'address']


class WarehouseSimpleSerializer(serializers.ModelSerializer):
    shortName = serializers.CharField(source='name')

    class Meta:
        model = Warehouse
        fields = ['id', 'shortName']


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    shortName = serializers.CharField(source="name")
    parent = serializers.CharField(source='parent.name', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'shortName', 'parent']


class SubCategoryRecursiveSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class CategorySerializerTree(serializers.ModelSerializer):
    subcategories = SubCategoryRecursiveSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'subcategories')


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
    inflow_total_count = serializers.SerializerMethodField()
    inflow_total_sum = serializers.SerializerMethodField()
    outflow_total_count = serializers.SerializerMethodField()
    outflow_total_sum = serializers.SerializerMethodField()
    start_balance_count = serializers.SerializerMethodField()
    start_balance_sum = serializers.SerializerMethodField()
    end_balance_count = serializers.SerializerMethodField()
    end_balance_sum = serializers.SerializerMethodField()

    def get_inflow_total_count(self, instance):
        return instance.inflow_total_count if instance.inflow_total_count else ''

    def get_inflow_total_sum(self, instance):
        return instance.inflow_total_sum if instance.inflow_total_sum else ''

    def get_outflow_total_count(self, instance):
        return instance.outflow_total_count if instance.outflow_total_count else ''

    def get_outflow_total_sum(self, instance):
        return instance.outflow_total_sum if instance.outflow_total_sum else ''

    def get_start_balance_count(self, instance):
        return instance.start_balance_count if instance.start_balance_count else ''

    def get_start_balance_sum(self, instance):
        return instance.start_balance_sum if instance.start_balance_sum else ''

    def get_end_balance_count(self, instance):
        return instance.end_balance_count if instance.end_balance_count else ''

    def get_end_balance_sum(self, instance):
        return instance.end_balance_sum if instance.end_balance_sum else ''

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