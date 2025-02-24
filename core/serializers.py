# serializers.py
from rest_framework import serializers
from .models import ValveStateHistory, ValveControl, WaterMeter

class WaterMeterSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterMeter
        fields = ['id', 'meter_no', 'user_code']
        
       

class ValveControlSerializer(serializers.ModelSerializer):
    state_display = serializers.CharField(source='get_state_display', read_only=True)
    
    class Meta:
        model = ValveControl
        fields = ['id', 'state', 'state_display', 'command_status', 'timestamp']

class ValveStateHistorySerializer(serializers.ModelSerializer):
    meter = WaterMeterSerializer(read_only=True)
    valve_control = ValveControlSerializer(read_only=True)
    previous_state_display = serializers.CharField(source='get_previous_state_display', read_only=True)
    new_state_display = serializers.CharField(source='get_new_state_display', read_only=True)
    changed_by_username = serializers.CharField(source='changed_by.username', read_only=True)

    class Meta:
        model = ValveStateHistory
        fields = [
            'id',
            'meter',
            'valve_control',
            'previous_state',
            'previous_state_display',
            'new_state',
            'new_state_display',
            'changed_at',
            'changed_by_username',
            'reason',
            'command_status'
        ]