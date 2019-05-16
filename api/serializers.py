from rest_framework import serializers
from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order

        # la variable fields permet de filtrer les champs du modèle à sérialiser
        fields = '__all__'  # pour le detail
        # fields = ('marketplace', 'idFlux', 'order_purchase_date', 'billing_email')  # pour l'index, si possible

        # la variable depth permet de serializer les objets enfants jusqu'à cette profondeur (0 si non renseigné)
        depth = 1
