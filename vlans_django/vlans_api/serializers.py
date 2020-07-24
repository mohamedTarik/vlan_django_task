from rest_framework import serializers
from .models import Vlans


class VlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vlans
        fields = '__all__'

