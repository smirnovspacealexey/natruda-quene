from django.core.management.base import BaseCommand, CommandError
from shaw_queue.models import Order, Servery, DeliveryOrder, Customer
from django.utils import timezone
import logging

logger_debug = logging.getLogger('debug_logger')


class Command(BaseCommand):

    def handle(self, *args, **options):
       print('--------START---------')

       delivery_orders = DeliveryOrder.objects.filter(obtain_timepoint__gte=timezone.datetime.today().date(),
                                                      order__close_time__isnull=True).order_by('delivered_timepoint')
       logger_debug.info(f'delivery_orders{timezone.datetime.today()} \n{delivery_orders}')
       for delivery_order in delivery_orders:
          for order in delivery_order.order.ordercontent_set.all():
              logger_debug.info(f'{order} {order.menu_item.get_cooking_time()}')
       print('this')

       print('---------END----------')
