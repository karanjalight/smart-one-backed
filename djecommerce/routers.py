from rest_framework import routers
from core.viewsets import *
router = routers.DefaultRouter()
from accounts.viewsets import *
from core.viewsets import *



router.register(r'users', RegisterUserViewSet)
router.register(r'water-meters', WaterMeterViewSet)
router.register(r'valve-controls', ValveControlViewSet)
router.register(r'valve-history', ValveStateHistoryViewSet)


