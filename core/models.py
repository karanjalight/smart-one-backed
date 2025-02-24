from django.db import models
from django.utils.timezone import now
from django.utils.text import slugify
import uuid
from django.conf import settings

class AuthenticationToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    access_token = models.CharField(max_length=255, unique=True)
    expires_in = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  

    
    def is_expired(self):
        return (now() - self.created_at).total_seconds() > self.expires_in

class WaterMeter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    meter_no = models.CharField(max_length=50, unique=True)
    user_code = models.CharField(max_length=50)
    signal_strength = models.FloatField()
    last_reading = models.FloatField(default=0.0)
    last_read_time = models.DateTimeField(null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.meter_no)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Meter {self.meter_no} - User {self.user_code}"

class MeterReading(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    meter = models.ForeignKey(WaterMeter, on_delete=models.CASCADE, related_name="readings")
    reading = models.FloatField()
    timestamp = models.DateTimeField()
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.meter.meter_no}-{self.timestamp}")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.meter.meter_no} - {self.reading} m³ at {self.timestamp}"

class ValveControl(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    VALVE_STATES = [
        (0, "Off"), (1, "On"), (2, "Force Off"),
        (3, "Force On"), (4, "Unlock")
    ]
    meter = models.ForeignKey(WaterMeter, on_delete=models.CASCADE, related_name="valve_controls")
    state = models.IntegerField(choices=VALVE_STATES)
    command_status = models.IntegerField(choices=[(0, "Success"), (1, "Failed")], default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.meter.meter_no}-{self.timestamp}-{self.state}")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Valve {self.get_state_display()} for {self.meter.meter_no} at {self.timestamp}"




class ValveStateHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    meter = models.ForeignKey('WaterMeter', on_delete=models.CASCADE, related_name='valve_history')
    valve_control = models.ForeignKey('ValveControl', on_delete=models.CASCADE, related_name='state_history')
    previous_state = models.IntegerField(choices=ValveControl.VALVE_STATES, null=True, blank=True)
    new_state = models.IntegerField(choices=ValveControl.VALVE_STATES)
    changed_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    reason = models.TextField(blank=True)  # Optional field to store reason for change
    command_status = models.IntegerField(
        choices=[(0, "Success"), (1, "Failed")],
        default=0
    )
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.meter.meter_no}-{self.changed_at}-{self.new_state}")
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"Valve state changed from {self.get_previous_state_display() or 'Initial'} "
            f"to {self.get_new_state_display()} for {self.meter.meter_no} "
            f"at {self.changed_at}"
        )

    class Meta:
        ordering = ['-changed_at']
        verbose_name_plural = "Valve state histories"