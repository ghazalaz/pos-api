
from rest_framework.response import Response
from rest_framework import status
from bonus.serializers import *
from bonus.models import MenuItem, Order, OrderItem
from rest_framework import viewsets


class ModifierGroupViewSet(viewsets.ModelViewSet):
    queryset = ModifierGroup.objects.all()
    serializer_class = ModifierGroupSerializer


class ModifierItemViewSet(viewsets.ModelViewSet):
    queryset = ModifierItem.objects.all()
    serializer_class = ModifierItemSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"id": response.data['id']}, status=status.HTTP_201_CREATED)

