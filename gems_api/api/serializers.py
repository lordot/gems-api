from rest_framework import serializers
from .models import Deal


class CSVImportSerializer(serializers.Serializer):
    csv_file = serializers.FileField()


class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = '__all__'


class TopSerializer(serializers.Serializer):
    username = serializers.CharField(source='customer')
    spent_money = serializers.IntegerField()
