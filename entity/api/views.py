from rest_framework import generics, permissions
from .serializers import *
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework import generics
from rest_framework import viewsets


class AreaList(generics.ListAPIView):

    serializer_class = AreaSerializer

    def get_queryset(self):
        # aa = Area.objects.all()
        # serializers = AreaSerializer(aa, many=True)
        return JSONRenderer().render({'aa': 'bb'})