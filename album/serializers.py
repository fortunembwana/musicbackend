from rest_framework import serializers
from songs.models import Song
from artists.models import Artist  
from .models import Album, AlbumSong


class CreateAlbumSerializer(serializers.ModelSerializer):
    artist = serializers.PrimaryKeyRelatedField(
        queryset=Artist.objects.all()
    )

    class Meta:
        model = Album
        fields = [
            'album_id',
            'album_name',
            'artist',
            'cover_image',
            'release_date',
            'description'
        ]
        read_only_fields = ['album_id']


class AlbumListSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source='artist.stage_name', read_only=True)
    number_of_songs = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = ['album_id', 'album_name', 'artist_name', 'cover_image', 'number_of_songs', 'release_date']    

    def get_number_of_songs(self, obj):
        return obj.songs.count()
    

class AlbumDetailSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source='artist.stage_name', read_only=True)

    class Meta:
        model = Album
        fields = ['album_id', 'album_name', 'artist_name', 'cover_image', 'number_of_songs', 'release_date', 'description']







