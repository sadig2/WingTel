from rest_framework import serializers
from .models import DataUsageRecord, VoiceUsageRecord
from django.db.models import Avg, Sum


class DataUsageRecordSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = DataUsageRecord
        fields = ['id', 'price','usage_date','kilobytes_used', 'total_price']

    def get_total_price(self, obj):
        return DataUsageRecord.objects.all().aggregate(Sum('price'))['price__sum']


class VoiceUsageRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceUsageRecord
        fields = '__all__'

    def create(self, validated_data):
        instance = VoiceUsageRecord.objects.create(**validated_data)
        return instance

    def to_representation(self, instance):
        original_representation = super().to_representation(instance)
        representation = {
            'total_price': self.get_total_price(instance),
            'detail': original_representation
        }
        return representation

    def get_total_price(self, obj):
        agr = VoiceUsageRecord.objects.all().aggregate(
            total_price=Sum('price'))
        return agr['total_price']
