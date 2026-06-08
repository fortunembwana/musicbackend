from rest_framework import serializers

from .models import Artist

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['artist_id', 'full_name', 'stage_name', 'phone_number', 'bio', 'profile_image', 'email']
        read_only_fields = ['artist_id', 'created_at', 'added_by', 'is_verified', 'updated_at']

 

class ArtistListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['artist_id', 'full_name', 'stage_name', 'email', 'is_verified']

   

class ArtistDetailSerializer(serializers.ModelSerializer):
    added_by = serializers.SerializerMethodField()
    approved_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = [
            'artist_id',
            'stage_name',
            'email',
            'phone_number',
            'bio',
            'profile_image',
            'is_verified',
            'approved',
            'approved_note',
            'created_at',
            'updated_at',
            'added_by',
            'approved_by_name'
        ]

    def get_added_by(self, obj):
        if not obj.added_by:
            return None

        user = obj.added_by
        return user.get_full_name() or user.username

    def get_approved_by_name(self, obj):
        if not obj.approved_by:
            return None

        user = obj.approved_by
        return user.get_full_name() or user.username