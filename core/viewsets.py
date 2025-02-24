from rest_framework import serializers
from .models import WaterMeter, MeterReading, ValveControl, ValveStateHistory
from django.contrib.auth import get_user_model
from rest_framework import  viewsets
from .models import *
from .serializers import *


User = get_user_model()


class WaterMeterViewSet(viewsets.ModelViewSet):
    queryset = WaterMeter.objects.all()
    serializer_class = WaterMeterSerializer
    
class ValveControlViewSet(viewsets.ModelViewSet):
    queryset = ValveControl.objects.all()
    serializer_class = ValveControlSerializer

class ValveStateHistoryViewSet(viewsets.ModelViewSet):
    queryset = ValveStateHistory.objects.all()
    serializer_class = ValveStateHistorySerializer

