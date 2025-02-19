from rest_framework import routers
from core.viewsets import *
router = routers.DefaultRouter()
from accounts.viewsets import *



router.register(r'users', RegisterUserViewSet)



