# niceauth/admin.py

from django.contrib import admin
from .models import NiceAuthRequest, NiceAuthResult

@admin.register(NiceAuthRequest)
class NiceAuthRequestAdmin(admin.ModelAdmin):
    list_display = ('request_no', 'created_at', 'updated_at')
    search_fields = ('request_no',)

@admin.register(NiceAuthResult)
class NiceAuthResultAdmin(admin.ModelAdmin):
    list_display = ('request', 'created_at', 'updated_at')
    search_fields = ('request__request_no',)
