from django.conf.urls import url, include
from django.urls import path, re_path
from rest_framework import routers
from api.views import *


router = routers.DefaultRouter()
router.register(r'punkt', PunktViewSet)
router.register(r'reservierung', ReservierungViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
]
