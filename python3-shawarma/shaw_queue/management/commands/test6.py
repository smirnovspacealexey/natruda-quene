from django.core.management.base import BaseCommand, CommandError
from apps.delivery.models import DeliveryHistory
from shaw_queue.models import Order
from shaw_queue.views import send_order_to_1c


class Command(BaseCommand):
    def handle(self, *args, **options):
        order = Order.objects.filter(pk=2013947).last()
        order.pk = None
        order.save()
        print(order)
        print(send_order_to_1c(order, False, True))
        print('\n')




