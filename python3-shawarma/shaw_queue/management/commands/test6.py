from django.core.management.base import BaseCommand, CommandError
from apps.delivery.models import DeliveryHistory
from shaw_queue.models import Order, OrderContent
from shaw_queue.views import send_order_to_1c


class Command(BaseCommand):
    def handle(self, *args, **options):
        order = Order.objects.filter(pk=2012074).last()
        curr_order_content = OrderContent.objects.filter(order=order, menu_item__price__gt=0)
        order.pk = None
        order.save()
        order.guid_1c = ''
        order.save()
        print(order)

        for oc in curr_order_content:
            print(oc.pk, oc.order.pk, '|')
            oc.pk = None
            oc.save()
            oc.order = order
            oc.save()
            print(oc.pk, oc.order.pk)

        print(send_order_to_1c(order, False, True))
        print('\n')




