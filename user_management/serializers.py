from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User

# Mixins for common fields across serializers
class FullNameMixin:
    full_name = serializers.SerializerMethodField(read_only=True)

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class AddedByMixin:
    added_by = serializers.SerializerMethodField(read_only=True)

    def get_added_by(self, obj):
        user = obj.added_by
        if not user:
            return None
        full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
        return full_name or user.username
    
# User serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'bio', 'profile_image', 'role']
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)

        if password:
            user.set_password(password)
            user.password_changed_at = timezone.now()  # Set password changed timestamp
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserListSerializer(FullNameMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'role', 'email']


class UserDetailSerializer(FullNameMixin, AddedByMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone_number', 'bio', 'profile_image', 'role', 'date_joined', 'is_active', 'is_staff', 'added_by']
      

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        token['role'] = user.role
        return token
    