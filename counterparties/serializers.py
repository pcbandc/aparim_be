from rest_framework import serializers
from .models import Counterparty


class CounterpartySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    shortName = serializers.CharField(source='short_name')
    fullName = serializers.CharField(source='full_name')

    class Meta:
        model = Counterparty
        fields = ['id', 'edrpou', 'shortName', 'fullName', 'address']