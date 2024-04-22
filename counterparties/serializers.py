from rest_framework import serializers
from .models import Counterparty, Agreement, ContactPerson, Contact


class CounterpartySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    shortName = serializers.CharField(source='short_name')
    fullName = serializers.CharField(source='full_name')

    class Meta:
        model = Counterparty
        fields = ['id', 'edrpou', 'shortName', 'fullName', 'address']


class AgreementSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')

    class Meta:
        model = Agreement
        fields = ['public_id', 'short_name', 'number', 'commencement_date',
                  'expiration_date', 'payment_delay_days', 'total_value',
                  'counterparty', 'type', 'description']


class ContactPersonSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')

    class Meta:
        model = ContactPerson
        fields = ['public_id', 'short_name', 'agreement', 'full_name',
                  'position', 'notes']


class ContactSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')

    class Meta:
        model = Contact
        fields = ['public_id', 'short_name', 'contact_person', 'type',
                  'value', 'notes']