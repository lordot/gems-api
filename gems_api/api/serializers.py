from rest_framework import serializers

from .models import Customer, Deal, Item


class CSVImportSerializer(serializers.Serializer):
    csv_file = serializers.FileField()


class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = ['total', 'quantity', 'date']


class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        min_length=4, max_length=15, allow_blank=False
    )

    class Meta:
        model = Customer
        fields = ['username']


class ItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        min_length=4, max_length=15, allow_blank=False
    )

    class Meta:
        model = Item
        fields = ['name']


class TopSerializer(serializers.Serializer):
    username = serializers.CharField()
    spent_money = serializers.IntegerField()
    gems = serializers.ListField()
