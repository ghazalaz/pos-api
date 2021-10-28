from rest_framework import serializers

from store.models import MenuItem, OrderItem, Order

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('menu_item', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField(label='items')
    # items = OrderItemSerializer(many=True, label="items")
    paid = serializers.DecimalField(max_digits=10, decimal_places=2)
    note = serializers.CharField(allow_null=True, default=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            if self.context['request'].method in ['POST']:
                self.fields['items'] = OrderItemSerializer(many=True, label="items")
            # if self.context['request'].method in ['GET']:
            #     self.fields['items'] = serializers.SerializerMethodField(label='items')
        except KeyError:
            pass

    class Meta:
        model = Order
        fields = ('id', 'items', 'paid', 'note')

    def create(self, validated_data):
        try:
            order = Order.objects.create(note=validated_data['note'], paid=validated_data['paid'], status=Order.Status.CREATED)
            items = validated_data['items']
            for item in items:
                OrderItem.objects.create(menu_item=item['menu_item'], quantity=item['quantity'], order=order)
            validated_data['id'] = order.id
            return validated_data
        except:
            raise serializers.ValidationError("Order failed")

    def validate(self, data):
        if not data['items']:
            raise serializers.ValidationError({"items": "Order items cannot be empty"})
        items = data['items']
        for item in items:
            if item['menu_item'].quantity < item['quantity'] or item['quantity'] <= 0:
                raise serializers.ValidationError({'item': item, 'error': "Invalid quantity"})
        order_amount = sum([item['menu_item'].price * item['quantity'] for item in items])
        if data['paid'] < order_amount:
            raise serializers.ValidationError({"paid": "Paid amount is incorrect"})

        return data

    def get_items(self, instance):
        items = OrderItem.objects.filter(order=instance)
        return OrderItemSerializer(items, many=True).data


class MenuItemSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField(min_value=0, default=0)
    quantity = serializers.IntegerField(min_value=0, default=0)
    class Meta:
        model = MenuItem
        fields = ('id', 'name', 'price', 'quantity', 'description')