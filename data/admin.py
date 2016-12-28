from django.contrib import admin
from .models import Image, File, AreaHousingPrice
# Register your models here.


class AreaHousingPriceAdmin(admin.ModelAdmin):
    list_display = ('area_name', 'dealAvgPrice', 'saleAvgPrice', 'total', 'date', 'data_source')
    list_filter = ('area_name', 'date', 'data_source')
    search_fields = ('area_name',)


admin.site.register(Image)
admin.site.register(File)
admin.site.register(AreaHousingPrice, AreaHousingPriceAdmin)
