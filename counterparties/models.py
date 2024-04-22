from django.db import models
import uuid

AGREEMENT_TYPES = {
    "VR": "Vendor",
    "CR": "Customer",
    "BK": "Bank",
    "CN": "Commissioner",
    "OR": "Other"
}

CONTACT_TYPES = {
    "CP": "City phone",
    "MP": "Mobile phone",
    "EM": "e-mail",
    "AS": "Address",
    "SN": "Social network",
    "OR": "Other"
}


class Counterparty(models.Model):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4)
    short_name = models.CharField(max_length=100, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    edrpou = models.CharField(unique=True, max_length=10)
    address = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.short_name} ({self.edrpou})'


class Agreement(models.Model):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4)
    short_name = models.CharField(max_length=100)
    number = models.CharField(max_length=30, blank=True, null=True)
    commencement_date = models.DateField()
    expiration_date = models.DateField()
    payment_delay_days = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    total_value = models.DecimalField(default=0, max_digits=14, decimal_places=2)
    counterparty = models.ForeignKey(Counterparty, on_delete=models.CASCADE, related_name='agreements')
    type = models.CharField(max_length=32, choices=AGREEMENT_TYPES)
    description = models.TextField()

    def __str__(self):
        return self.short_name


class ContactPerson(models.Model):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4)
    short_name = models.CharField(max_length=100)
    agreement = models.ForeignKey(Agreement, on_delete=models.CASCADE, related_name='persons')
    full_name = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    notes = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.short_name


class Contact(models.Model):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4)
    short_name = models.CharField(max_length=100)
    contact_person = models.ForeignKey(ContactPerson, on_delete=models.CASCADE, related_name='contacts')
    type = models.CharField(max_length=32, choices=AGREEMENT_TYPES)
    value = models.CharField(max_length=100, blank=True, null=True)
    notes = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.short_name



