from wingtel.sprint_subscriptions.models import SprintSubscription
from django.http import HttpResponse
from rest_framework import viewsets
from wingtel.sprint_subscriptions.serializers import SprintSubscriptionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum


class SprintSubscriptionViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides `retrieve`, `create`, and `list` actions.
    """
    queryset = SprintSubscription.objects.all()
    serializer_class = SprintSubscriptionSerializer


# /api/sprint_subscriptions/{id}/sub_by_id/
# looks for specific sprintsubscription by id, aggregates related data_record's field -> price

    @action(detail=True, methods=['get', ])
    def sub_by_id(self, request, pk=None):
        sub = SprintSubscription.objects.get(id=pk)
        data_record_price = sub.data_usage_record.all()\
            .aggregate(Sum('price'))['price__sum']
        serializer = self.get_serializer(sub)
        result = serializer.data
        result['total_price'] = data_record_price
        return Response(result)
