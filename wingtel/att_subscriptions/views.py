from rest_framework import mixins, viewsets
from rest_framework.response import Response

from wingtel.att_subscriptions.models import ATTSubscription
from wingtel.att_subscriptions.serializers import ATTSubscriptionSerializer
from django.db.models import Q
from wingtel.usage.models import DataUsageRecord, VoiceUsageRecord


class ATTSubscriptionViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides `retrieve`, `create`, and `list` actions.
    """
    queryset = ATTSubscription.objects.all()
    serializer_class = ATTSubscriptionSerializer
    """
    List a queryset if Usage price is greater that parameter
    """
    def list(self, request, *args, **kwargs):
        limit = self.request.query_params.get('limit')
        data = DataUsageRecord.objects.filter(price__gt=limit)
        voice = VoiceUsageRecord.objects.filter(price__gt=limit)

        queryset1 = ATTSubscription.objects.filter(data_usage_record__in=data)
        queryset2 = ATTSubscription.objects.filter(
            voice_usage_record__in=voice)

        queryset = queryset1 | queryset2

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
