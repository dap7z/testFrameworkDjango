from django.db import models

# Create your models here.
# Models allow data persistence and validation
# https://www.webforefront.com/django/modeldatatypesandvalidation.html


class Order(models.Model):
    ID_TXT_LENGTH = 19

    marketplace = models.CharField(max_length=255)
    idFlux = models.PositiveIntegerField()
    order_id = models.CharField(max_length=ID_TXT_LENGTH, primary_key=True)
    order_mrid = models.CharField(max_length=ID_TXT_LENGTH)
    order_refid = models.CharField(max_length=ID_TXT_LENGTH)
    order_purchase_date = models.DateField(default=None, null=True)
    order_purchase_heure = models.TimeField(default=None, null=True)
    order_amount = models.FloatField(null=False)
    order_currency = models.CharField(max_length=3)
    # cart, ect.


class TrackingInformations(models.Model):
    tracking_shipped_date = models.DateTimeField(default=None, null=True)
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        null=False,
        primary_key=True,
    )
    # (OneToOneField dans Order fonctionne mais recreer à chaque update une ligne dans TrackingInformations...)

