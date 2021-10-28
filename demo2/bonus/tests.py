from collections import OrderedDict

from rest_framework.test import APITestCase
from rest_framework import status

from bonus.models import *


class OrderCreateTestCase(APITestCase):
    def setUp(self):
        MenuItem.objects.create(
            price=15,
            description="Pizza",
            quantity=10
        )
        MenuItem.objects.create(
            price=15,
            description="Burger",
            quantity=10
        )
        group = ModifierGroup.objects.create(
            name="Toppings"
        )
        ModifierItem.objects.create(
            group=group,
            name="Onions"
        )
        ModifierItem.objects.create(
            group=group,
            name="Pickles"
        )

    def test_create_order(self):
        initial_order_count = Order.objects.count()
        menu_items = MenuItem.objects.all()
        group = ModifierGroup.objects.all().first()
        modifier_items = ModifierItem.objects.all()

        order_attrs = {
            "items": [
                {
                    "menu_item": menu_items[0].id,
                    "quantity": 5,
                    "modifiers_list": [
                        {
                            "group": group.id,
                            "items": [modifier_items[0].id,modifier_items[1].id]
                        }
                    ]
                },
                {
                    "menu_item": menu_items[1].id,
                    "quantity": 7,
                    "modifiers_list": [
                        {
                            "group": group.id,
                            "items": [modifier_items[0].id]
                        }
                    ]
                }
            ],
            "paid": 200,
            "note": "Thanks"
        }
        response = self.client.post('/api/v1/orders/', order_attrs, "json")
        if response.status_code != status.HTTP_201_CREATED:
            print(response.data)
        self.assertEqual(
            Order.objects.count(), initial_order_count + 1
        )

