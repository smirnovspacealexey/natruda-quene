from django.core.management.base import BaseCommand, CommandError
from shaw_queue.models import Order, Servery, DeliveryOrder, Customer
from django.utils import timezone
import logging

logger_debug = logging.getLogger('debug_logger')


class Command(BaseCommand):

    def handle(self, *args, **options):
       print('--------START---------')

       # order = Order.objects.create(
       #     daily_number=11,
       #     open_time=timezone.now(),
       #     with_shawarma=True,
       #     shashlyk_completed=True,
       #     supplement_completed=True,
       #     start_shawarma_preparation=True,
       #     start_shawarma_cooking=True,
       #     total=100,
       #     is_paid=True,
       #     pickup=True,
       #     # is_delivery=True,
       #     from_site=True,
       #     # is_grilling=True,
       #     servery=Servery.objects.first(),
       #
       # )
       # print(order)
       # print(DeliveryOrder.objects.create(order=order, daily_number=11, customer=Customer.objects.first()))
       logger_debug.info(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
       print('this')

       print('---------END----------')
