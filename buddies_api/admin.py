from django.contrib import admin
from .models import Ihrd

@admin.register(Ihrd)
class IhrdAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'nickname', 'place', 'date_of_birth')
    search_fields = ('full_name', 'nickname', 'place')