from rest_framework import serializers
from .models import Song
from artists.serializers import UserSerializer

class SongSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source='artist.stage_name', read_only=True)

    class Meta:
        model = Song
        fields = ['id', 'title', 'genre', 'cover_image', 'audio_file', 
                  'description', 'payment_status', 'approval_status', 
                  'streams', 'uploaded_at', 'artist_name']
        read_only_fields = ['payment_status', 'approval_status', 'streams']