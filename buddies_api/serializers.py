from rest_framework import serializers
from .models import Ihrd

class IhrdSerializer(serializers.ModelSerializer):
    # Formats database field outputs to match what your React app expects
    DOB = serializers.DateField(source='date_of_birth', format='%Y-%m-%d', required=False, allow_null=True)
    Full_Name = serializers.CharField(source='full_name')

    class Meta:
        model = Ihrd
        fields = ['id', 'Full_Name', 'nickname', 'place', 'DOB', 'image_url']
