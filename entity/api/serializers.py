from rest_framework import serializers
from entity.models import *


class AreaSerializer(serializers.ModelSerializer):
    higher = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='areas-detail',
    )
    # lower = serializers.HyperlinkedIdentityField(view_name='entity_areas')

    class Meta:
        model = Area
        fields = ('id', 'name', 'level', 'code', 'higher')
