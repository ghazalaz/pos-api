from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from store import api_views

router = routers.DefaultRouter()
router.register(r'api/v1/orders', api_views.OrderViewSet, basename="orders")
router.register(r'api/v1/menu-items', api_views.MenuItemViewSet, basename="menuitems")

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
