from django.conf.urls import url, include
from django.urls import path, re_path
from rest_framework import routers
import api.views.reservierungs_view as rv
import api.views.punkt_view as pv

router = routers.DefaultRouter()
router.register(r'punkt', pv.PunktViewSet)
router.register(r'reservierung', rv.ReservierungViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
]
