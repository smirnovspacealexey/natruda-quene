from django.core.management.base import BaseCommand, CommandError
from shaw_queue.models import Order, Servery, DeliveryOrder, Customer, OrderContent
from django.utils import timezone
from django.contrib.sessions.models import Session


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('--------START---------')
        popular = {}
        i = 10000
        for order_content in OrderContent.objects.all().order_by('-pk')[:10000]:
            note = order_content.note
            i = i - 1
            print(f'{i}) {order_content.menu_item.title}   {note}')
            if note:
                if note in popular:
                    popular[note] = note + 1
                else:
                    popular.update({note: 1})
        print(popular)
        print('---------END----------')


