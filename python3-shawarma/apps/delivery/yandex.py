from .models import DeliveryHistory, YandexSettings
from shaw_queue.models import ServicePoint
import requests
import json
from apps.sms.backend import send_sms
import logging

logger_debug = logging.getLogger('debug_logger')


url = 'https://b2b.taxi.yandex.net/b2b/cargo/integration/v2/claims/'

'https://3dsec.sberbank.ru/payment/merchants/sbersafe_sberid/payment_ru.html?mdOrder=696e0967-a32c-7785-875d-62c928b640d7'


def delivery_request(order, source, destination, history=None):
    yandex_settings = YandexSettings.current()
    headers = {'Accept-Language': 'ru', 'Authorization': 'Bearer ' + yandex_settings.token}

    if not history:
        history = DeliveryHistory.objects.create()

    cargo_options = []
    if yandex_settings.thermobag:
        cargo_options.append('thermobag')

    if yandex_settings.auto_courier:
        cargo_options.append('auto_courier')

    items = []

    for item in order.ordercontent_set.all():
        items.append(
            {
                "cost_currency": yandex_settings.currency,
                "cost_value": str(item.menu_item.price),
                "droppof_point": 2,
                "extra_id": order.daily_number,
                "pickup_point": 1,
                "quantity": item.quantity,
                "size": {
                    "height": 0.05,
                    "length": 0.1,
                    "width": 0.1
                },
                "title": item.menu_item.title,
                "weight": item.menu_item.category.weight
            }
        )

    data = {
        "client_requirements": {
            "assign_robot": yandex_settings.assign_robot,
            "pro_courier": yandex_settings.taxi_class,
            "taxi_class": yandex_settings.taxi_class,
            "cargo_options": cargo_options
        },
        "comment": "",
        "emergency_contact": {
            "name": source.title,
            "phone": source.phone
        },
        "items": items,
        "optional_return": yandex_settings.optional_return,
        "referral_source": yandex_settings.referral_source,
        "route_points": [
            {
                "address": {
                    "coordinates": [
                        source.longitude,  # Longitude
                        source.latitude   # Latitude
                    ],
                    "fullname": source.fullname,
                    "building": source.building,
                    "building_name": source.building_name,
                    "city": source.city,
                    "comment": source.comment,
                    "country": source.country,
                    "description": source.description,
                    # "door_code": "169",
                    # "door_code_extra": "Код на вход во двор № 1234, код от апартаментов № 4321",
                    # "doorbell_name": "Волк",
                    "porch": source.porch,
                    "sflat": source.sflat,
                    "sfloor": source.sfloor
                },
                "contact": {
                    "email": yandex_settings.email,
                    "name": source.title,
                    "phone": source.phone
                },
                "external_order_cost": {
                    "currency": yandex_settings.currency,
                    "currency_sign": yandex_settings.currency_sign,
                    "value": order.total
                },
                "external_order_id": order.daily_number,
                "pickup_code": history.six_numbers,
                "point_id": 1,
                "skip_confirmation": yandex_settings.skip_confirmation,
                "type": "source",
                "visit_order": 1
            },
            {
                "address": {
                    # "coordinates": [
                    #     37.307115,
                    #     55.634146
                    # ],
                    "fullname": destination["fullname"],
                    "building": destination["building"],
                    "building_name": destination["building_name"],
                    "city": destination["city"],
                    "comment": destination["comment"],
                    "country": destination["country"],
                    "description": destination["description"],
                    "door_code": destination["door_code"],
                    "door_code_extra": destination["door_code_extra"],
                    "doorbell_name": destination["doorbell_name"],
                    "porch": destination["porch"],
                    "sflat": destination["sflat"],
                    "sfloor": destination["sfloor"]
                },
                "contact": {
                    "email": destination['email'],
                    "name": destination['name'],
                    "phone": destination['phone']
                },
                "external_order_cost": {
                    "currency": yandex_settings.currency,
                    "currency_sign": yandex_settings.currency_sign,
                    "value": order.total
                },
                "external_order_id":  order.daily_number,
                "point_id": 2,
                "skip_confirmation": yandex_settings.skip_confirmation,
                "type": "destination",
                "visit_order": 2
            }
        ],
        "skip_act": yandex_settings.skip_act,
        "skip_client_notify": yandex_settings.skip_client_notify,
        "skip_door_to_door": yandex_settings.skip_door_to_door,
        "skip_emergency_notify": yandex_settings.skip_emergency_notify
    }

    res = requests.post(f'{url}create?request_id={history.request_id}', json=data, headers=headers)
    response = json.loads(res.content.decode("utf-8"))
    print(res.status_code)
    print(response)
    # if res.status_code == 200:

    logger_debug.info(f'delivery_request {headers} \n {data} \n {res.status_code} \n {response}')

