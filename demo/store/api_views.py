
from rest_framework.response import Response
from rest_framework import status
from store.serializers import MenuItemSerializer, OrderSerializer, OrderItemSerializer
from store.models import MenuItem, Order, OrderItem
from rest_framework import viewsets


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def list(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"id":response.data['id']}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializers = self.get_serializer(instance)
        return Response(serializers.data)