from django.core.management.base import BaseCommand, CommandError
from shaw_queue.models import Order, Servery, DeliveryOrder, Customer
from django.utils import timezone
import logging

logger_debug = logging.getLogger('debug_logger')


class Command(BaseCommand):

    def handle(self, *args, **options):
       print('--------START---------')
       logger_debug.info(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
       print('this')

       print('---------END----------')
