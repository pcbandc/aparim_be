import uuid
from datetime import datetime
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from counterparties.models import Counterparty, Agreement

WAREHOUSE_TYPES = {
    'WS': 'Wholesale',
    'RL': 'Retail',
    'PT': 'Post operator',
    'CT': 'Consignment'
}
VAT_RATES = {
    '20%': '20%',
    '7%': '7%',
    '0%': '0%',
    'w/VAT': 'без ПДВ',
    'not VAT': 'не ПДВ'
}
GOOD_TRANSACTION_TYPE = {
    'RT': 'Receipt',
    'DH': 'Dispatch',
    'CN': 'Credit note',
    'DN': 'Debit note',
    'WO': 'Write off',
    'MT': 'Moving goods to',
    'MF': 'Moving goods from',

}
DOCUMENT_TYPE = {
    "PI": "Purchase invoice",
    "SI": "Sales invoice",
    "CN": "Credit note",
    "DN": "Debit note"
}


class Warehouse(models.Model):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=12, choices=WAREHOUSE_TYPES)
    active = models.BooleanField(default=True)
    address = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'


class Category(MPTTModel):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True,
                            blank=True, related_name='children')

    def __str__(self):
        return f'{self.name}'


class Uom(models.Model):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4)
    short_name = models.CharField(max_length=10, unique=True)
    full_name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.short_name}'


class Good(models.Model):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4)
    short_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=200)
    outer_id = models.CharField(max_length=50, blank=True, null=True)
    uktzed = models.CharField(max_length=50, blank=True, null=True)
    basic_uom = models.ForeignKey(Uom, on_delete=models.CASCADE)
    vat_rate = models.CharField(max_length=12, choices=VAT_RATES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.short_name}'


class StockCard(models.Model):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4)
    time = models.DateTimeField(default=datetime.now())
    good = models.ForeignKey(Good, on_delete=models.CASCADE,
                             related_name='cards')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE,
                                  related_name='cards')
    balance = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.id} - {self.good}'


class Document(models.Model):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4)
    counterparty = models.ForeignKey(Counterparty, on_delete=models.CASCADE,
                                     related_name='counterparties')
    agreement = models.ForeignKey(Agreement, on_delete=models.CASCADE,
                                  related_name='agreements')
    type = models.CharField(choices=DOCUMENT_TYPE, max_length=12)
    time = models.DateTimeField()
    number = models.CharField(max_length=50)
    posted = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f'{self.number} dd {self.time}'


class DocumentLine(models.Model):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4)
    good = models.ForeignKey(Good, on_delete=models.CASCADE,
                             related_name='lines')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE,
                                  related_name='lines', default=1)
    document = models.ForeignKey(Document, on_delete=models.CASCADE,
                                 related_name='lines')
    quantity = models.DecimalField(max_digits=10, decimal_places=3)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    vat_rate = models.CharField(max_length=12, choices=VAT_RATES)

    def __str__(self):
        return f'{self.document} - {self.good}'


class GoodTransaction(models.Model):
    public_id = models.UUIDField(db_index=True, unique=True,
                                 default=uuid.uuid4)
    good = models.ForeignKey(Good, on_delete=models.CASCADE,
                             related_name='transactions')
    card = models.ForeignKey(StockCard, on_delete=models.CASCADE,
                             related_name='transactions')
    document = models.ForeignKey(Document, on_delete=models.CASCADE,
                                 related_name='transactions')
    document_line = models.ForeignKey(DocumentLine, on_delete=models.CASCADE,
                                      related_name='transactions')
    transaction_type = models.CharField(max_length=12,
                                        choices=GOOD_TRANSACTION_TYPE)
    quantity = models.DecimalField(max_digits=10, decimal_places=3)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.document}'