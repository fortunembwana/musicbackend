from rest_framework import serializers
from django.contrib.auth.models import User  
from .models import Artist

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ArtistRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Artist
        fields = ['username', 'email', 'password', 'stage_name', 'phone_number', 'bio']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        artist = Artist.objects.create(
            user=user,
            stage_name=validated_data['stage_name'],
            phone_number=validated_data['phone_number'],
            bio=validated_data.get('bio', '')
        )
        return artist