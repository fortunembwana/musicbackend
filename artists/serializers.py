from rest_framework import serializers

from .models import Artist

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['artist_id', 'stage_name', 'phone_number', 'bio', 'profile_image', 'username', 'email']
        read_only_fields = ['artist_id', 'created_at', 'added_by']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data.pop('added_by', None)  # Remove added_by if it's in the validated data
        if request and hasattr(request, 'user'):
            validated_data['added_by'] = request.user  # Set added_by to the current user
        return super().create(validated_data)

class ArtistListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Artist
        fields = ['artist_id', 'stage_name']

   

class ArtistDetailSerializer(serializers.ModelSerializer):
    added_by = serializers.SerializerMethodField(read_only=True)

    def get_added_by(self, obj):
        user = obj.added_by
        if not user:
            return None
        full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
        return full_name or user.username

    class Meta:
        model = Artist
        fields = ['artist_id', 'stage_name', 'phone_number', 'bio', 'profile_image', 'is_verified', 'created_at', 'added_by']