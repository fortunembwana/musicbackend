from django.http import FileResponse
from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Song
from .serializers import (
    CreateSongSerializer,
    SongListSerializer,
    SongDetailSerializer
)


class SongCreateView(generics.CreateAPIView):
    queryset = Song.objects.all()
    serializer_class = CreateSongSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]


class SongListView(generics.ListAPIView):
    queryset = Song.objects.filter(
        approval_status='approved'
    )
    serializer_class = SongListSerializer
    permission_classes = [permissions.AllowAny]


class SongDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    serializer_class = SongDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'song_id'


class SongDownloadView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, song_id):
        song = get_object_or_404(
            Song,
            song_id=song_id,
            approval_status='approved'
        )

        song.download_count += 1
        song.save(update_fields=['download_count'])

        response = FileResponse(
            song.audio_file.open('rb'),
            as_attachment=True
        )

        response['Content-Disposition'] = (
            f'attachment; filename="{song.title}.mp3"'
        )

        return response


class SongStreamView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, song_id):
        song = get_object_or_404(
            Song,
            song_id=song_id,
            approval_status='approved'
        )

        song.streams += 1
        song.save(update_fields=['streams'])

        response = FileResponse(song.audio_file.open('rb'))
        response['Content-Type'] = 'audio/mpeg'
        response['Accept-Ranges'] = 'bytes'

        return response