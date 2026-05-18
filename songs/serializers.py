from rest_framework import serializers
from .models import Song

class SongSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source='artist.stage_name', read_only=True)
    download_url = serializers.SerializerMethodField()
    stream_url = serializers.SerializerMethodField()

    class Meta:
        model = Song
        fields = ['id', 'title', 'genre', 'cover_image', 'audio_file', 
                  'description', 'payment_status', 'approval_status', 
                  'streams', 'downloads', 'uploaded_at', 'artist_name',
                  'download_url', 'stream_url']
        read_only_fields = ['payment_status', 'approval_status', 'streams', 'downloads']

    def get_download_url(self, obj):
        if obj.approval_status == 'approved':
            return f"/api/songs/download/{obj.id}/"
        return None

    def get_stream_url(self, obj):
        if obj.approval_status == 'approved':
            return f"/api/songs/stream/{obj.id}/"
        return None