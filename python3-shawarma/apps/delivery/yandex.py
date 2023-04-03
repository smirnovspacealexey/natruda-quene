from .models import DeliveryHistory, YandexSettings
from shaw_queue.models import ServicePoint
import requests
import json


url = 'https://b2b.taxi.yandex.net/b2b/cargo/integration/v2/claims/'


def delivery_request(history=None):
    if not history:
        history = DeliveryHistory.objects.create()

    # data = {
    #     "same_day_data": {
    #         "delivery_interval": {
    #             "from": "2022-07-09T09:00:00+00:00",
    #             "to": "2022-07-09T13:00:00+00:00"
    #         }
    #     },
    #     "client_requirements": {
    #         "assign_robot": false,
    #         "pro_courier": false,
    #         "taxi_class": "courier",
    #         "cargo_options": [
    #             "thermobag",
    #             "auto_courier"
    #         ]
    #     },
    #     "comment": "Осторожно — в корзине пирожки!",
    #     "emergency_contact": {
    #         "name": "Красная Шапочка",
    #         "phone": "+79123456789"
    #     },
    #     "items": [
    #         {
    #             "cost_currency": "RUB",
    #             "cost_value": "200.00",
    #             "droppof_point": 2,
    #             "extra_id": "БП-208",
    #             "pickup_point": 1,
    #             "quantity": 1,
    #             "size": {
    #                 "height": 0.05,
    #                 "length": 0.1,
    #                 "width": 0.1
    #             },
    #             "title": "Пирожки с картошкой",
    #             "weight": 0.3
    #         }
    #     ],
    #     "optional_return": false,
    #     "referral_source": "bitrix",
    #     "route_points": [
    #         {
    #             "address": {
    #                 "coordinates": [
    #                     37.312082,  # Longitude
    #                     55.634253   # Latitude
    #                 ],
    #                 "fullname": "Москва, деревня Рассказовка, ул. Сказочная, д. 5",
    #                 "building": "5",
    #                 "building_name": "Дом Волка",
    #                 "city": "Москва",
    #                 "comment": "Калитка открыта, постучать в дверь три раза, топнуть ногой и повернуться три раза вокруг себя",
    #                 "country": "Российская Федерация",
    #                 "description": "Москва, Россия",
    #                 "door_code": "169",
    #                 "door_code_extra": "Код на вход во двор № 1234, код от апартаментов № 4321",
    #                 "doorbell_name": "Волк",
    #                 "porch": "A",
    #                 "sflat": "1",
    #                 "sfloor": "1"
    #             },
    #             "contact": {
    #                 "email": "shapka@failytail.ru",
    #                 "name": "Красная Шапочка",
    #                 "phone": "+79123456789"
    #             },
    #             "external_order_cost": {
    #                 "currency": "RUB",
    #                 "currency_sign": "₽",
    #                 "value": "200.0"
    #             },
    #             "external_order_id": "100",
    #             "pickup_code": "893422",
    #             "point_id": 1,
    #             "skip_confirmation": false,
    #             "type": "source",
    #             "visit_order": 1
    #         },
    #         {
    #             "address": {
    #                 "coordinates": [
    #                     37.307115,
    #                     55.634146
    #                 ],
    #                 "fullname": "Москва, деревня Рассказовка, ул. Сказочная, д. 1",
    #                 "building": "16",
    #                 "building_name": "Дом Бабушки",
    #                 "city": "Москва",
    #                 "comment": "Бабушка спит, подойти к окну и прокричать 3 раза, что вы курьер от Яндекса",
    #                 "country": "Российская Федерация",
    #                 "description": "Москва, Россия",
    #                 "door_code": "169",
    #                 "door_code_extra": "Домофон у бабушки не работает",
    #                 "doorbell_name": "Бабушка",
    #                 "porch": "A",
    #                 "sflat": "1",
    #                 "sfloor": "1"
    #             },
    #             "contact": {
    #                 "email": "babushka@failytail.ru",
    #                 "name": "Бабушка",
    #                 "phone": "+79876543210"
    #             },
    #             "external_order_cost": {
    #                 "currency": "RUB",
    #                 "currency_sign": "₽",
    #                 "value": "200.0"
    #             },
    #             "external_order_id": "100",
    #             "point_id": 2,
    #             "skip_confirmation": true,
    #             "type": "destination",
    #             "visit_order": 2
    #         }
    #     ],
    #     "skip_act": false,
    #     "skip_client_notify": false,
    #     "skip_door_to_door": false,
    #     "skip_emergency_notify": false
    # }

    res = requests.post(f'{url}create?request_id={history.request_id}', data=data)
    response = json.loads(res.content.decode("utf-8"))
    print(res.status_code)
    print(response)
    # if res.status_code == 200:

