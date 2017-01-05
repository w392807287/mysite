from django.contrib import admin
from .models import Proxy

# Register your models here.


class ProxyAdmin(admin.ModelAdmin):
    list_display = ('address', 'position', 'anonymity', 'type')
    list_filter = ('anonymity', 'type')
    search_fields = ('address', 'position',)

admin.site.register(Proxy, ProxyAdmin)