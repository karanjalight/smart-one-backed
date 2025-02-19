from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.
admin.site.site_header = "SMART ONE ADMIN"
admin.site.site_title = "SMART ONE ADMIN"
admin.site.index_title = "SMART ONE - Administration"
