from rest_framework.viewsets import ModelViewSet
from .models import DataUsageRecord, VoiceUsageRecord
from .serializers import DataUsageRecordSerializer, VoiceUsageRecordSerializer
from django.db.models import Avg
from rest_framework.decorators import action
from rest_framework.response import Response


class DataUsageRecordViewSet(ModelViewSet):

    queryset = DataUsageRecord.objects.all()
    serializer_class = DataUsageRecordSerializer


class VoiceUsageRecordViewSet(ModelViewSet):

    queryset = VoiceUsageRecord.objects.all()
    serializer_class = VoiceUsageRecordSerializer

    @action(detail=False)
    def aggregated(self, request):
        vr = VoiceUsageRecord.objects.all().aggregate(Avg('price'))
        page = self.paginate_queryset(vr)
        if page is not None:
            serializer = self.get_serializer(vr, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(vr, many=True)
        return Response(serializer.data)
