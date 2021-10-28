from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, permissions

from bonus import api_views

router = routers.DefaultRouter()
router.register(r'api/v1/orders', api_views.OrderViewSet, basename="orders")
router.register(r'api/v1/order-items', api_views.OrderItemViewSet, basename="order-items")
router.register(r'api/v1/menu-items', api_views.MenuItemViewSet, basename="menu-items")
router.register(r'api/v1/modifier/items', api_views.ModifierItemViewSet, basename="modifier-items")
router.register(r'api/v1/modifier/groups', api_views.ModifierGroupViewSet, basename="modifier-groups")

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
