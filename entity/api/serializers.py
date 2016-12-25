from rest_framework import serializers
from entity.models import *


class AreaSerializer(serializers.ModelSerializer):
    # higher = serializers.HyperlinkedIdentityField(
    #     view_name='entity_areas',
    #     lookup_field='name',
    # )

    class Meta:
        model = Area
        fields = ('id', 'name', 'level', 'code', 'higher', )
