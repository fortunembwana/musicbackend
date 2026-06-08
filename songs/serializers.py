from curses import meta
from datetime import timedelta
from user_management.serializers import FullNameMixin, AddedByMixin
from rest_framework import serializers, generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from album.models import Album
from artists.models import Artist
from .models import Song, Category

def get_quality(bitrate):
    if bitrate >= 320:
        return 'High'
    elif bitrate >= 192:
        return 'Medium'
    return 'Low'


def get_audio_metadata(file):
    try:
        from mutagen import File as MutagenFile

        audio = MutagenFile(file)

        bitrate = (
            audio.info.bitrate // 1000
            if hasattr(audio.info, 'bitrate')
            else None
        )

        duration = (
            audio.info.length
            if hasattr(audio.info, 'length')
            else None
        )

        return bitrate, duration

    except Exception:
        return None, None
    
def get_duration_in_minutes(duration):
    if duration is None:
        return None
    total_seconds = duration.total_seconds()
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    return f"{minutes}:{seconds:02d}"

def get_file_size_in_mb(file_size):
    if file_size is None:
        return None
    size_in_mb = file_size / (1024 * 1024)
    return f"{size_in_mb:.2f} MB"

def get_audio_metadata(file):
    try:
        from mutagen import File as MutagenFile
        audio = MutagenFile(file)
        bitrate = audio.info.bitrate // 1000  # Convert to kbps
        duration = audio.info.length  # Duration in seconds
        return bitrate, duration
    except Exception as e:
        print(f"Error extracting metadata: {e}")
        return None, None



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'name']
        read_only_fields = ['category_id']


class CreateSongSerializer(serializers.ModelSerializer):

    album = serializers.PrimaryKeyRelatedField(
        queryset=Album.objects.all(),
        required=False,
        allow_null=True
    )

    genre = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Song
        fields = [
            'song_id',
            'title',
            'album',
            'genre',
            'cover_image',
            'audio_file',
            'description',
            'year_released'
        ]

        read_only_fields = [
            'song_id'
        ]

    def validate_audio_file(self, value):
        allowed = ['mp3', 'wav', 'flac']

        extension = value.name.split('.')[-1].lower()

        if extension not in allowed:
            raise serializers.ValidationError(
                "Only mp3, wav and flac files are allowed."
            )

        return value

    def create(self, validated_data):
        request = self.context['request']

        artist = Artist.objects.get(
            user=request.user
        )

        audio_file = validated_data.get('audio_file')

        bitrate, duration = get_audio_metadata(
            audio_file
        )

        validated_data['artist'] = artist
        validated_data['added_by'] = request.user

        validated_data['bitrate'] = bitrate

        if duration:
            validated_data['duration'] = timedelta(
                seconds=int(duration)
            )

        validated_data['quality'] = (
            get_quality(bitrate)
            if bitrate
            else None
        )

        validated_data['file_size'] = (
            audio_file.size
            if audio_file
            else None
        )

        validated_data['file_type'] = (
            audio_file.name.split('.')[-1].lower()
            if audio_file
            else None
        )

        return Song.objects.create(
            **validated_data
        )


class SongListSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(
        source='artist.stage_name',
        read_only=True
    )

    album_title = serializers.CharField(
        source='album.album_name',
        read_only=True
    )

    genre_name = serializers.CharField(
        source='genre.name',
        read_only=True
    )

    class Meta:
        model = Song
        fields = [
            'song_id',
            'title',
            'artist_name',
            'album_title',
            'genre_name',
            'cover_image',
            'download_count'
        ]

class SongDetailSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(
        source='artist.stage_name',
        read_only=True
    )

    album_title = serializers.CharField(
        source='album.album_name',
        read_only=True
    )

    genre_name = serializers.CharField(
        source='genre.name',
        read_only=True
    )

    class Meta:
        model = Song

        fields = [
            'song_id',
            'title',
            'artist_name',
            'album_title',
            'genre_name',
            'cover_image',
            'description',
            'payment_status',
            'approval_status',
            'file_type',
            'file_size',
            'bitrate',
            'quality',
            'streams',
            'downloads',
            'created_at'
        ]


class SongUploadView(generics.CreateAPIView):
    queryset = Song.objects.all()
    serializer_class = CreateSongSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]



# def generate_waveform(duration_seconds):
#     import numpy as np
#     import matplotlib.pyplot as plt
#     # Simulate audio data for demonstration purposes
#     time = np.linspace(0, duration_seconds, num=1000)
#     amplitude = np.sin(2 * np.pi * 5 * time)  # Simulated sine wave
#     # Generate waveform image
#     plt.figure(figsize=(10, 2))
#     plt.plot(time, amplitude)
#     plt.axis('off')
#     plt.tight_layout()
#     # Save to a bytes buffer
#     from io import BytesIO
#     buffer = BytesIO()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)
#     return buffer



# class CreateSongSerializer(serializers.ModelSerializer):
#     artist= serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all(), write_only=True)
#     album = serializers.PrimaryKeyRelatedField(queryset=Album.objects.all(), required=False, allow_null=True)
#     category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False, allow_null=True)
#     download_url = serializers.SerializerMethodField()
#     stream_url = serializers.SerializerMethodField()

#     class Meta:
#         model = Song
#         fields = ['song_id', 'artist', 'title', 'genre', 'cover_image', 'audio_file', 
#                   'description', 'album']
#         read_only_fields = ['payment_status', 'approval_status', 'streams', 'downloads',
#                             'file_size', 'file_type', 'bitrate', 'quality', 'waveform',
#                             'song_id']

#     def get_download_url(self, obj):
#         if obj.approval_status == 'approved':
#             return f"/api/songs/download/{obj.id}/"
#         return None

#     def get_stream_url(self, obj):
#         if obj.approval_status == 'approved':
#             return f"/api/songs/stream/{obj.id}/"
#         return None
    
#     def create(self, validated_data):
#         request = self.context.get('request')
#         validated_data.pop('added_by', None)  # Remove added_by if it's in the validated data
#         if request and hasattr(request, 'user'):
#             validated_data['added_by'] = request.user  # Set added_by to the current user
        
#         audio_file = validated_data.get('audio_file')

#         bitrate, duration = get_audio_metadata(audio_file)

#         validated_data['bitrate'] = bitrate

#         if duration:
#             validated_data['duration'] = timedelta(
#                 seconds=int(duration)
#             )

#             validated_data['quality'] = (
#                 get_quality(bitrate)
#                 if bitrate
#                 else None
#             )

#             validated_data['file_size'] = (
#                 audio_file.size
#                 if audio_file
#                 else None
#             )

#             validated_data['file_type'] = (
#                 audio_file.name.split('.')[-1]
#                 if audio_file
#                 else None
#             )

#             return super().create(validated_data)
     

# class SongListSerializer(serializers.ModelSerializer):
#     artist_name = serializers.CharField(source='artist.stage_name', read_only=True)
#     album_title = serializers.CharField(source='album.album_name', read_only=True)

#     class Meta:
#         model = Song
#         fields = ['song_id', 'title', 'artist_name', 'album_title', 'genre', 'cover_image','download_count']

# class SongDetailSerializer(serializers.ModelSerializer):
#     artist_name = serializers.CharField(source='artist.stage_name', read_only=True)
#     album_title = serializers.CharField(source='album.album_name', read_only=True)

#     class Meta:
#         model = Song
#         fields = ['song_id', 'title', 'artist_name', 'album_title', 'genre', 'cover_image', 
#                   'description', 'payment_status', 'approval_status', 'file_type', 'file_size', 'bitrate', 'quality', 'waveform',
#                   'streams', 'downloads', 'uploaded_at']


