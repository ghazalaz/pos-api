from rest_framework.exceptions import ValidationError, ErrorDetail
from rest_framework.test import APITestCase
from rest_framework import status
from store.models import MenuItem, Order


class MenuItemCreateTestCase(APITestCase):
    def test_create_menu_item(self):
        initial_menu_item_count = MenuItem.objects.count()
        menu_item_attrs = {
            'price': 15,
            'description': "Pizza",
            'quantity': 10
        }
        response = self.client.post('/api/v1/menu-items/', menu_item_attrs)
        if response.status_code != status.HTTP_201_CREATED:
            print(response.data)

        self.assertEqual(
            MenuItem.objects.count(), initial_menu_item_count + 1
        )

        for attr, expected_value in menu_item_attrs.items():
            self.assertEqual(response.data[attr], expected_value)


class MenuItemDestroyTestCase(APITestCase):
    def setUp(self):
        MenuItem.objects.create(
            price=15,
            description="Pizza",
            quantity=10
        )

    def test_delete_menu_item(self):
        initial_menu_item_count = MenuItem.objects.count()
        menu_item_id = MenuItem.objects.first().id
        self.client.delete('/api/v1/menu-items/{}/'.format(menu_item_id))
        self.assertEqual(
            MenuItem.objects.count(), initial_menu_item_count - 1
        )
        self.assertRaises(
            MenuItem.DoesNotExist, MenuItem.objects.get, id=menu_item_id
        )


class MenuItemUpdateTestCase(APITestCase):
    def setUp(self):
        MenuItem.objects.create(
            price=15,
            description="Diet Coke",
            quantity=10
        )

    def test_update_menu_item(self):
        menu_item = MenuItem.objects.first()
        updated_menu_item = {
                'price': 20,
                'description': 'Diet Coke',
                'quantity': 50
            }
        response = self.client.patch(
            '/api/v1/menu-items/{}/'.format(menu_item.id),
            updated_menu_item
        )
        updated = MenuItem.objects.get(id=menu_item.id)
        self.assertEqual(updated.price, updated_menu_item['price'])
        self.assertEqual(updated.description, updated_menu_item['description'])
        self.assertEqual(updated.quantity, updated_menu_item['quantity'])


class OrderCreateTestCase(APITestCase):
    def setUp(self):
        MenuItem.objects.create(
            price="5.00",
            description="Diet Coke",
            quantity=10
        )
        MenuItem.objects.create(
            price="5.00",
            description="Water",
            quantity=10
        )

    def test_create_order(self):
        initial_count = Order.objects.count()
        menu_items = MenuItem.objects.all()
        order_attrs = {
            "items": [
                {"menu_item": menu_items[0].id, "quantity":1},
                {"menu_item": menu_items[1].id, "quantity":1}
            ],
            "paid": "10.00",
            "note": "No notes."
        }
        response = self.client.post('/api/v1/orders/', order_attrs, "json")
        if response.status_code != status.HTTP_201_CREATED:
            print(response.data)
        self.assertEqual(
            Order.objects.count(), initial_count + 1
        )
        order_obj = self.client.get('/api/v1/orders/{}/'.format(response.data['id']))
        for attr, expected_value in order_attrs.items():
            self.assertEqual(order_obj.data[attr], expected_value)

    def test_validate_paid(self):
        menu_items = MenuItem.objects.all()
        order_attrs = {
            "items": [
                {"menu_item": menu_items[0].id, "quantity": 1},
                {"menu_item": menu_items[1].id, "quantity": 1}
            ],
            "paid": "5.00",
            "note": "No notes."
        }
        response = self.client.post('/api/v1/orders/', order_attrs, "json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('paid',response.data.keys())

    def test_validate_items(self):
        order_attrs = {
            "items": [
            ],
            "paid": "0.00",
            "note": "No notes."
        }
        response = self.client.post('/api/v1/orders/', order_attrs, "json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('items', response.data.keys())

    def test_validate_availability(self):
        menu_items = MenuItem.objects.all()
        order_attrs = {
            "items": [
                {"menu_item": menu_items[0].id, "quantity": 11},
            ],
            "paid": "5.00",
            "note": "No notes."
        }
        response = self.client.post('/api/v1/orders/', order_attrs, "json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('item', response.data.keys())