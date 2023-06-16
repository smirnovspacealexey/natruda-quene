from django.core.management.base import BaseCommand, CommandError
from apps.delivery.models import DeliveryActive
from apps.delivery.backend import check_delivery_status, delivery_request, delivery_confirm
from shaw_queue.models import ServicePoint
import logging
import json
import time
import sys, traceback

logger_debug = logging.getLogger('debug_logger')


class Command(BaseCommand):
    help = 'Check delivery statuses'

    def handle(self, *args, **options):
        logger_debug.info(f'Check delivery statuses\n\n')

        for delivery in DeliveryActive.objects.all():
            if delivery.delivery.order and delivery.delivery.order.close_time:
                delivery.delete()
                continue

            if delivery.delivery.wait_minutes:
                wait_minutes = delivery.delivery.wait_minutes - 5
                logger_debug.info(wait_minutes)

                if wait_minutes < 1:
                    history = delivery.delivery
                    destination = {}
                    destination["fullname"] = history.fullname
                    destination['phone'] = history.phone
                    destination['longitude'] = history.longitude
                    destination['latitude'] = history.latitude
                    destination['city'] = history.city
                    destination['comment'] = history.comment
                    destination['country'] = history.country
                    destination['description'] = history.description
                    destination['door_code'] = history.door_code if history.door_code else ''
                    destination['porch'] = history.porch if history.porch else ''
                    destination['sflat'] = history.sflat if history.sflat else ''
                    destination['sfloor'] = history.sfloor if history.sfloor else ''

                    items = history.items
                    items = items.replace("\'", "\"")
                    items = list(json.loads(items))
                    logger_debug.info(history)

                    delivery_request(ServicePoint.objects.filter(id=2).last(), destination, history=history, items=items, price=history.full_price)
                    continue

                delivery.delivery.wait_minutes = wait_minutes
                delivery.delivery.save()
            check_delivery_status(delivery.delivery)

