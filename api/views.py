from orders.models import Order
from api import serializers
from rest_framework import viewsets
from url_filter.integrations.drf import DjangoFilterBackend


# Create your views here.


class OrderViewSet(viewsets.ModelViewSet):
    """
    https://django-url-filter.readthedocs.io/en/latest/
    url_filter.integrations.drf permet la recherche par l'url :
        /api/orders/?format=json&marketplace__icontains=disco
        /api/orders/?format=json&order_id__icontains=55m
        /api/orders/?format=json&order_purchase_date=2014-10-22
        /api/orders/?format=json&order_purchase_date__range=2010-01-01,2015-12-31
    """
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['order_id', 'marketplace', 'order_purchase_date']
