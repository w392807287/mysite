from rest_framework import serializers
from data.models import *


class AreaHousingPriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = AreaHousingPrice
        fields = ('area_name', 'dealAvgPrice', 'saleAvgPrice', 'total', 'date', 'data_source')