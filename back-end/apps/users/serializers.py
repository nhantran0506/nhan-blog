from rest_framework import serializers
from .model import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'username', 'email', 'birth_date', 'role')
        read_only_fields = ('user_id', 'role')

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'birth_date')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
