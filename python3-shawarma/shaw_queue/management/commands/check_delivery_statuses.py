from django.core.management.base import BaseCommand, CommandError
from apps.delivery.models import DeliveryActive
from apps.delivery.backend import check_delivery_status
import logging
import time
import sys, traceback

logger_debug = logging.getLogger('debug_logger')


class Command(BaseCommand):
    help = 'Check delivery statuses'

    def handle(self, *args, **options):
        logger_debug.info(f'Check delivery statuses\n\n')

        for delivery in DeliveryActive.objects.all():
            if delivery.delivery.order and not delivery.delivery.order.close_time:
                delivery.delete()
                continue

            check_delivery_status(delivery.delivery)

