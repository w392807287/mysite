from .serializers import *
from rest_framework import generics
from rest_framework import mixins


class AreaHousingPriceList(generics.ListCreateAPIView):
    serializer_class = AreaHousingPriceSerializer
    queryset = AreaHousingPrice.objects.all()

