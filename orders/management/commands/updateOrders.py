from django.core.management.base import BaseCommand, CommandError
from orders.models import Order, TrackingInformations
from tqdm import tqdm
import requests
import xml.etree.ElementTree as ET
import datetime
import pytz


class Command(BaseCommand):
    """
    Permet l'integration en base de données de fichiers xml au format suivant :
       <statistics ip="xx.xx.xx.xx" server="LengowTest" timeGenerated="2015-07-01 00:00:00.652336" version="2.1">
           <orders_count>
               <count_total>5</count_total>
               <count_by_marketplace>...</count_by_marketplace>
               <count_by_status>...</count_by_status>
           </orders_count>
           <orders>
               <order>...</order>
               <order>...</order>
           </orders>
       </statistics>
    """
    help = "Mise à jour des commandes à partir des données xml"

    def handle(self, *args, **options):
        response = requests.get('http://test.lengow.io/orders-test.xml')
        self.stdout.write('xml récupéré, début du traitement')

        # On recupere les éléments principaux du xml
        elem_statistics = ET.fromstring(response.content)
        elem_orders_count = elem_statistics[0]
        elem_orders = elem_statistics[1]

        # On verifie que le nombre de commande correspond à celui indiqué
        nb_orders_expected: int = int(elem_orders_count.find('count_total').text)
        nb_orders_calc = len(elem_orders)
        if nb_orders_calc != nb_orders_expected:
            raise CommandError('Count error, '
                               + 'nb_orders_calc: ' + str(nb_orders_calc)
                               + 'nb_orders_expected: ' + str(nb_orders_expected))

        # On creer une progress bar
        progress_bar = tqdm(desc="Processing", total=nb_orders_expected)

        # On parcourt les commandes contenu dans le xml
        for elem_order in elem_orders:
            # On initialise le model
            model_order = Order()
            model_tracking_informations = None
            for child in elem_order:
                # On recupère ce qui nous interesse
                if hasattr(model_order, child.tag):
                    value = self.value_from_xml(child)
                    setattr(model_order, child.tag, value)
                elif child.tag == 'tracking_informations':
                    model_tracking_informations = self.value_from_xml(child)
            # On met à jour la bdd grâce au model
            model_order.save()
            model_tracking_informations.order = model_order
            model_tracking_informations.save()
            progress_bar.update(1)

        # Si aucune exception ne s'est déclenchée :
        progress_bar.close()
        self.stdout.write(self.style.SUCCESS('Travail terminé !'))

    ####################################################################################################################

    @classmethod
    def parse_datetime(cls, datetime_str, datetime_format):
        if datetime_str is None:
            return None
        datetime_obj = datetime.datetime.strptime(datetime_str, datetime_format)
        return datetime_obj

    @classmethod
    def value_from_xml(cls, xml):
        # pas de switch en python :(
        if xml.tag == 'marketplace':
            return xml.text
        if xml.tag == 'idFlux':
            return int(xml.text)
        elif xml.tag == 'order_id':
            return xml.text
        elif xml.tag == 'order_mrid':
            return xml.text
        elif xml.tag == 'order_refid':
            return xml.text
        elif xml.tag == 'order_purchase_date':
            # exemple: 2014-10-21
            my_date = cls.parse_datetime(xml.text, '%Y-%m-%d')
            if my_date is not None:
                my_date = pytz.utc.localize(my_date)
                my_date = my_date.date()
            return my_date
        elif xml.tag == 'order_purchase_heure':
            # exemple: 14:59:51
            my_time = cls.parse_datetime(xml.text, '%H:%M:%S')
            if my_time is not None:
                my_time = pytz.utc.localize(my_time)
                my_time = my_time.time()
            return my_time
        elif xml.tag == 'tracking_informations':
            tracking_informations = TrackingInformations()
            # exemple: 2015-01-20 16:01:01
            my_datetime = cls.parse_datetime(
                xml.find('tracking_shipped_date').text,
                '%Y-%m-%d %H:%M:%S')
            # l'API ne l'indique pas, mais on suppose que c'est de l'UTC donc on l'indique avant l'enregistrement :
            if my_datetime is not None:
                my_datetime = pytz.utc.localize(my_datetime)
            tracking_informations.tracking_shipped_date = my_datetime
            return tracking_informations
        elif xml.tag == 'order_amount':
            return float(xml.text)
        elif xml.tag == 'order_currency':
            return xml.text
        else:
            raise CommandError(xml.tag + ' present dans le model mais pas géré dans la fonction value_from_xml()')
