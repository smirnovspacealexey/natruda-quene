from django.core.management.base import BaseCommand, CommandError
from apps.delivery.models import DeliveryHistory
from shaw_queue.models import Order, OrderContent
from shaw_queue.views import send_order_to_1c
from apps.logs.models import Log
import requests
import sys, traceback


class Command(BaseCommand):
    def handle(self, *args, **options):

        try:

            order_dict = {'servery_number': 'c5adbbec-45e8-11e8-a151-00155d004a00', 'cash': True, 'cashless': False,
                          'internet_order': False, 'queue_number': '1', 'cook': '  ', 'return_of_goods': False,
                          'total': 60.0, 'DC': '111', 'Discount': '0', 'Goods': [
                    {'Name': '2 Бон Аква 0,5', 'Count': 1, 'GUID': '82e54530-767f-11e6-82c6-28c2dd30392b',
                     'QR': ""}]}

            if args[0] == '1':
                order_dict = {'servery_number': 'c5adbbec-45e8-11e8-a151-00155d004a00', 'cash': True, 'cashless': False, 'internet_order': False, 'queue_number': '1', 'cook': '  ', 'return_of_goods': False, 'total': 60.0, 'DC': '111', 'Discount': '0', 'Goods': [{'Name': '2 Бон Аква 0,5', 'Count': 1, 'GUID': '82e54530-767f-11e6-82c6-28c2dd30392b', 'QR': "0104610011500015215G*,D'y_Kk!WL93/8tP"}, {'Name': '2 Бон Аква 0,5', 'Count': 1, 'GUID': '82e54530-767f-11e6-82c6-28c2dd30392b', 'QR': '0104610011500039215ecb.JGNF84F793LSr6'}]}
            if args[0] == '2':
                order_dict = {'servery_number': 'c5adbbec-45e8-11e8-a151-00155d004a00', 'cash': True, 'cashless': False, 'internet_order': False, 'queue_number': '15', 'cook': ' ', 'return_of_goods': False, 'total': 60.0, 'DC': '111', 'Discount': '0', 'Goods': [{'Name': '2 Бон Аква 0,5', 'Count': 1, 'GUID': '82e54530-767f-11e6-82c6-28c2dd30392b', 'QR': '0104610011500039215ecb.JGNF84F793LSr6'}]}
            if args[0] == '3':
                order_dict = {'servery_number': 'c5adbbec-45e8-11e8-a151-00155d004a00', 'cash': True, 'cashless': False, 'internet_order': False, 'queue_number': '3', 'cook': ' ', 'return_of_goods': False, 'total': 60.0, 'DC': '111', 'Discount': '0', 'Goods': [{'Name': '2 Бон Аква 0,5', 'Count': 1, 'GUID': '82e54530-767f-11e6-82c6-28c2dd30392b', 'QR': '0104610011500015215?doldg5xTKXm93a1mC'}]}
            if args[0] == '4':
                order_dict = {'servery_number': 'c5adbbec-45e8-11e8-a151-00155d004a00', 'cash': True, 'cashless': False, 'internet_order': False, 'queue_number': '2', 'cook': ' ', 'return_of_goods': False, 'total': 60.0, 'DC': '111', 'Discount': '0', 'Goods': [{'Name': '2 Бон Аква 0,5', 'Count': 1, 'GUID': '82e54530-767f-11e6-82c6-28c2dd30392b', 'QR': '0104610011500015215jrhEG7SbQSSj93uAU8'}]}

            result = requests.post(
                'http://192.168.20.75:80/NaTruda/hs/Exchange/',
                auth=("b'Obmen'", '111'),
                json=order_dict)
            print(result)
        except:
            print(f'ERROR: {traceback.format_exc()}')

    def add_arguments(self, parser):
        parser.add_argument(nargs='*',
                            type=str,
                            dest='args',
                            help='ex: '
                            )




