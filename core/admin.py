from django.contrib import admin
from .models import *

@admin.register(AuthenticationToken)
class AuthenticationTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'access_token', 'expires_in', 'created_at', 'is_expired')
    search_fields = ('user__username', 'access_token')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)

@admin.register(WaterMeter)
class WaterMeterAdmin(admin.ModelAdmin):
    list_display = ('id', 'meter_no', 'user_code', 'signal_strength', 'last_reading', 'last_read_time')
    search_fields = ('meter_no', 'user_code')
    list_filter = ('last_read_time',)
    prepopulated_fields = {'slug': ('meter_no',)}

@admin.register(MeterReading)
class MeterReadingAdmin(admin.ModelAdmin):
    list_display = ('id', 'meter', 'reading', 'timestamp')
    search_fields = ('meter__meter_no',)
    list_filter = ('timestamp',)
    prepopulated_fields = {'slug': ('meter', 'timestamp')}

@admin.register(ValveControl)
class ValveControlAdmin(admin.ModelAdmin):
    list_display = ('id', 'meter', 'state', 'command_status', 'timestamp')
    search_fields = ('meter__meter_no',)
    list_filter = ('state', 'command_status', 'timestamp')
    prepopulated_fields = {'slug': ('meter', 'state')}

admin.site.register(ValveStateHistory)