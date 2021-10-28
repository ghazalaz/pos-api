from collections import defaultdict

from rest_framework import serializers

from bonus.models import MenuItem, OrderItem, Order, ModifierGroup, ModifierItem, OrderModifier


class MenuItemSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField(min_value=0, default=0)
    quantity = serializers.IntegerField(min_value=0, default=0)
    class Meta:
        model = MenuItem
        fields = ('id', 'name', 'price', 'quantity', 'description')


class ModifierGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModifierGroup
        fields = ('id', 'name')


class ModifierItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModifierItem
        fields = ('id', 'name', 'group')

    def validate(self, data):
        if not data['group']:
            raise serializers.ValidationError({"group": "Invalid group id"})
        return data


class OrderModifierSerializer(serializers.Serializer):
    class Meta:
        model = OrderModifier
        fields = ('id', 'group', 'item')


class OrderItemSerializer(serializers.ModelSerializer):
    modifiers_list = serializers.SerializerMethodField(label='modifiers_list')

    class Meta:
        model = OrderItem
        fields = ('id','menu_item', 'quantity', 'modifiers_list')

    def validate(self, data):
        return data

    def get_modifiers_list(self, instance):
        queryset = OrderModifier.objects.filter(order_item=instance).values('group','item').order_by()
        items = defaultdict(list)
        for row in queryset:
            items[row['group']].append(row['item'])
        result = []
        for item in items:
            result.append({"group":item, "items":items[item]})
        return result


class CustomOrderModifierGroupSerializer(serializers.Serializer):
    group = serializers.IntegerField()
    items = serializers.ListField()

    def validate(self, data):
        group_id = data['group']
        for modifier_id in data['items']:
            obj = ModifierItem.objects.get(id=modifier_id)
            if obj.group.id != group_id:
                raise serializers.ValidationError({"items"})
        return data


class CustomOrderItemSerializer(serializers.ModelSerializer):
    modifiers_list = CustomOrderModifierGroupSerializer(many=True)

    class Meta:
        model = OrderItem
        fields = ('menu_item', 'quantity', 'modifiers_list')


class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField(label='items')
    paid = serializers.DecimalField(max_digits=10, decimal_places=2)
    note = serializers.CharField(allow_null=True, default=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            if self.context['request'].method in ['POST']:
                self.fields['items'] = CustomOrderItemSerializer(many=True, label="items")
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
                order_item = OrderItem.objects.create(order=order,menu_item=item['menu_item'], quantity=item['quantity'])
                for modifier in item['modifiers_list']:
                    group_id = modifier['group']
                    for modifier_id in modifier['items']:
                        OrderModifier.objects.create(order_item=order_item, group_id=group_id, item_id=modifier_id)
            validated_data['id'] = order.id
            return validated_data
        except Exception as e:
            raise serializers.ValidationError("Order failed")

    def validate(self, data):
        if not data['items']:
            raise serializers.ValidationError({"items": "Order items cannot be empty"})
        items = data['items']
        for item in items:
            if item['menu_item'].quantity < item['quantity']:
                raise serializers.ValidationError({'item': item, 'error': "Invalid quantity"})
        order_amount = sum([item['menu_item'].price * item['quantity'] for item in items])
        if data['paid'] < order_amount:
            raise serializers.ValidationError({"paid": "Paid amount is incorrect"})

        return data

    def get_items(self, instance):
        items = OrderItem.objects.filter(order=instance)
        return OrderItemSerializer(items, many=True).data
