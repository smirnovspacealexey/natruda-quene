from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from shaw_queue.models import Order
import logging

logger_debug = logging.getLogger('debug_logger')


def sber_result(request):
    daily_number = request.GET.get('daily_number')
    logger_debug.info(f'sber_result \n{request.GET}')
    if daily_number:
        order = Order.objects.filter(open_time__contains=timezone.now().date(),
                                     close_time__isnull=True, is_canceled=False, is_paid=False,
                                     is_ready=False, is_delivery=True, delivery_daily_number=int(daily_number))
        order.is_paid = True
        order.save()

        logger_debug.info(f'sber_result order \n{order}')
