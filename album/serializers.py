from rest_framework import serializers

from songs.models import Song
from .models import Album, AlbumSong


class CreateAlbumSerializer(serializers.ModelSerializer):
    song_ids = serializers.PrimaryKeyRelatedField(
        queryset=Song.objects.all(),
        many=True,
        write_only=True,
        required=False,
    )

    class Meta:
        model = Album
        fields = [
            'album_id',
            'album_name',
            'artist',
            'cover_image',
            'number_of_songs',
            'release_date',
            'description',
            'song_ids',
        ]
        read_only_fields = ['album_id', 'artist', 'number_of_songs']

    def create(self, validated_data):
        song_ids = validated_data.pop('song_ids', [])
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['artist'] = request.user.artist  # Set artist to the current user's artist profile

        album = super().create(validated_data)

        # Attach songs to the album after it is created.
        for song in song_ids:
            AlbumSong.objects.get_or_create(album=album, song=song)

        # Keep the number_of_songs field in sync.
        album.number_of_songs = album.album_songs.count()
        album.save(update_fields=['number_of_songs'])
        return album


class AlbumListSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source='artist.stage_name', read_only=True)

    class Meta:
        model = Album
        fields = ['album_id', 'album_name', 'artist_name', 'cover_image', 'number_of_songs', 'release_date']    

class AlbumDetailSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source='artist.stage_name', read_only=True)

    class Meta:
        model = Album
        fields = ['album_id', 'album_name', 'artist_name', 'cover_image', 'number_of_songs', 'release_date', 'description']


class CreateAlbumSongSerializer(serializers.ModelSerializer):
    album = serializers.PrimaryKeyRelatedField(queryset=Album.objects.all())
    song = serializers.PrimaryKeyRelatedField(queryset=Song.objects.all())
    class Meta:
        model = AlbumSong
        fields = ['album_song_id', 'album', 'song']
        read_only_fields = ['album_song_id']
