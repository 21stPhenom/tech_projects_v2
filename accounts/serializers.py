from rest_framework import serializers

from accounts.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'ranking', 'projects_completed')
        read_only_fields = ('id', 'ranking', 'projects_completed')
        extra_kwargs = {'password': {'write_only': True}}