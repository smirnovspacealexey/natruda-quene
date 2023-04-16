from .models import DeliveryHistory, YandexSettings
from shaw_queue.models import ServicePoint, Menu
import requests
import json
from apps.sms.backend import send_sms
import sys, traceback
import logging

logger_debug = logging.getLogger('debug_logger')


url = 'https://b2b.taxi.yandex.net/b2b/cargo/integration/v2/claims/'

'https://3dsec.sberbank.ru/payment/merchants/sbersafe_sberid/payment_ru.html?mdOrder=696e0967-a32c-7785-875d-62c928b640d7'


def delivery_request(source, destination, history=None, order=None, order_items=None, price=None):
    try:
        yandex_settings = YandexSettings.current()
        headers = {'Accept-Language': 'ru', 'Authorization': 'Bearer ' + yandex_settings.token}

        if not history:
            history = DeliveryHistory.objects.create(full_price=price)

        cargo_options = []
        if yandex_settings.thermobag:
            cargo_options.append('thermobag')

        if yandex_settings.auto_courier:
            cargo_options.append('auto_courier')

        items = []

        for item in order_items:
            menu_item = Menu.objects.filter(pk=item['id']).last()
            items.append(
                {
                    "cost_currency": yandex_settings.currency,
                    "cost_value": str(menu_item.price),
                    "droppof_point": 2,
                    "extra_id": str(item['id']),
                    "pickup_point": 1,
                    "quantity": item['quantity'],
                    "size": {
                        "height": 0.05,
                        "length": 0.1,
                        "width": 0.1
                    },
                    "title": menu_item.title,
                    "weight": menu_item.category.weight / 1000
                }
            )

        data = {
            "client_requirements": {
                "assign_robot": yandex_settings.assign_robot,
                "pro_courier": yandex_settings.pro_courier,
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
                        "value": str(price)
                    },
                    "external_order_id": history.daily_number,
                    "pickup_code": history.six_numbers,
                    "point_id": 1,
                    "skip_confirmation": yandex_settings.skip_confirmation,
                    "type": "source",
                    "visit_order": 1
                },
                {
                    "address": {
                        "coordinates": [
                            yandex_settings.longitude,  # Longitude
                            yandex_settings.latitude   # Latitude
                        ],
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
                        # "email": destination['email'],
                        "name": destination['name'],
                        "phone": destination['phone']
                    },
                    "external_order_cost": {
                        "currency": yandex_settings.currency,
                        "currency_sign": yandex_settings.currency_sign,
                        "value": str(price)
                    },
                    "external_order_id":  history.daily_number,
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
        if res.status_code == 200:
            return history.daily_number, history.six_numbers
        else:
            return None, None
    except:
        logger_debug.info(f'ERROR: {traceback.format_exc()}')

    # logger_debug.info(f'delivery_request {order, order.pk} \n\n{headers} \n {data} \n {res.status_code} \n {response}')

