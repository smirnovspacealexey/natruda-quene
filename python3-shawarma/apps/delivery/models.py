from django.utils import timezone
from django.db import models
from shaw_queue.models import Menu, Order
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
import random


def get_uuid():
    return str(uuid.uuid4())


def get_six_numbers():
    return str(random.randint(100000, 999999))


class DeliveryDistance(models.Model):
    meters = models.IntegerField(verbose_name="метров", default=0)
    roubles = models.IntegerField(verbose_name="цена", default=0)
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE, verbose_name="Menu Item", null=True, blank=True)

    def __str__(self):
        return f'{self.meters}m: {self.roubles}rub'


class DeliverySettings(models.Model):
    distances = models.ManyToManyField(DeliveryDistance, verbose_name="дистанции", blank=True)
    active = models.BooleanField('active', default=True)

    @staticmethod
    def current():
        return DeliverySettings.objects.filter(active=True).last()

    @staticmethod
    def get_js():
        ds = DeliverySettings.current()
        if not ds:
            return ''

        js = ''
        for distance in ds.distances.all().order_by('meters'):
            js += f'if ({distance.meters} > value) {{data["pk_delivery"] = {distance.menu_item.pk}; return {distance.roubles}}};'
        return js

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.active:
            type(self).objects.exclude(pk=self.pk).update(active=False)
        super().save()


class YandexSettings(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    token = models.CharField(verbose_name='OAuth-токен', max_length=200)
    geocoder_key = models.CharField(verbose_name='ключ геокодера', default=None, null=True, blank=True, max_length=200)
    active = models.BooleanField('active', default=True)

    assign_robot = models.BooleanField('assign_robot', default=False,
                                       help_text="Пытаться ли назначить заказ на ровер (шестиколесный робот)")

    pro_courier = models.BooleanField('pro_courier', default=False,
                                      help_text='Опция "Профи" для тарифов "Экспресс" и "Курьер"')

    taxi_class = models.CharField('taxi_class', default='courier', max_length=200,
                                  choices=[('courier', 'courier'), ('express', 'express'), ('cargo', 'cargo'), ],
                                  help_text='Класс такси. Возможные значения: courier, express, cargo')

    auto_courier = models.BooleanField('auto_courier', default=False, help_text='курьер только на машине')
    thermobag = models.BooleanField('thermobag', default=True, help_text='курьер с термосумкой')

    emergency_contact_name = models.CharField('emergency_contact_name', max_length=200, default='',
                                              help_text='Имя контактного лица')
    emergency_contact_phone = models.CharField(max_length=200, default='',
                                               help_text='Телефон контактного лица')

    optional_return = models.BooleanField('optional_return', default=False,
                                          help_text='Не требуется возврат товаров в случае отмены заказа.'
                                                    ' true - курьер оставляет товар себе,'
                                                    ' false - по умолчанию, требуется вернуть товар')

    referral_source = models.CharField(max_length=200, default='',
                                       help_text='Источник заявки (можно передать наименование CMS, из которой создается запрос)')

    skip_confirmation = models.BooleanField('skip_confirmation', default=False,
                                            help_text='Пропускать подтверждение через SMS в данной точке. False - подтверждение требуется')

    currency = models.CharField(max_length=200, default="RUB", help_text='Валюта расчёта')
    currency_sign = models.CharField(max_length=200, default="₽", help_text='Знак валюты')

    skip_act = models.BooleanField(default=False, help_text='Не показывать акт')
    skip_client_notify = models.BooleanField(default=False, help_text='Не отправлять отправителю/получателю смс-нотификации, когда к нему направится курьер.')
    skip_door_to_door = models.BooleanField(default=False, help_text='Отказ от доставки до двери (выключить опцию "От двери до двери").')
    skip_emergency_notify = models.BooleanField(default=False, help_text='Не отправлять нотификации emergency контакту')

    email = models.CharField(max_length=200, default="", help_text='Email')

    test_phone = models.CharField(max_length=200, default='', help_text='Телефон для тестового заказа')
    latitude = models.FloatField(verbose_name="тестовая Широта", default=55.196829, blank=False, null=False)
    longitude = models.FloatField(verbose_name="тестовая Долгота", default=61.395762, blank=False, null=False)

    def __str__(self):
        return self.name if self.name else f'id{self.pk}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.active:
            type(self).objects.exclude(pk=self.pk).update(active=False)
        super().save()

    @staticmethod
    def current():
        return YandexSettings.objects.filter(active=True).last()

    @staticmethod
    def OAuthToken():
        current = YandexSettings.current()
        if current:
            return current.token
        else:
            return ''

    @staticmethod
    def geocoder():
        current = YandexSettings.current()
        if current:
            return current.geocoder_key
        else:
            return ''


class DeliveryHistory(models.Model):
    uuid = models.CharField(max_length=200, default='')
    six_numbers = models.CharField('код для курьера', max_length=200, default="")
    daily_number = models.CharField('daily_number', max_length=50, default="")
    full_price = models.IntegerField(verbose_name="full_price", default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    confirm = models.BooleanField(default=False, help_text='заявка подтверждена')
    claim_id = models.CharField('claim_id', max_length=50, default="")
    # delivery_price = models.IntegerField(verbose_name="delivery_price", default=0)
    # description = models.CharField('description', max_length=500, default="")
    # coordinates = models.CharField('coordinates', max_length=100, default="")
    # porch = models.CharField('porch', max_length=100, default="")
    # door_code = models.CharField('door_code', max_length=100, default="")
    # sfloor = models.CharField('sfloor', max_length=100, default="")
    # sflat = models.CharField('sflat', max_length=100, default="")
    # comment = models.TextField(blank=True, null=True)
    # phone = models.CharField('phone', max_length=100, default="")
    # name = models.CharField('name', max_length=100, default="")
    # delivery_menu = models.ForeignKey(Menu, on_delete=models.SET_NULL, verbose_name="delivery_menu", null=True, blank=True)
    # items = models.TextField(blank=True, null=True)

    @property
    def request_id(self):
        return self.uuid + '-' + str(self.pk)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.six_numbers == '':
            self.six_numbers = get_six_numbers()

        if self.uuid == '':
            self.uuid = get_uuid()

        if self.daily_number == '':
            daily_number = None

            while daily_number is None:
                daily_number = get_six_numbers()
                if Order.objects.filter(open_time__contains=timezone.now().date(), daily_number=int(daily_number)).exists()\
                        or DeliveryHistory.objects.filter(daily_number=daily_number, confirm=False).exists():
                    daily_number = None

            self.daily_number = daily_number

        super().save()






