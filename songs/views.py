from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import FileResponse
from django.shortcuts import get_object_or_404

from .models import Song
from .serializers import SongSerializer
from artists.models import Artist


class SongUploadView(generics.CreateAPIView):
    """Artists upload songs"""
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        try:
            artist = Artist.objects.get(user=self.request.user)
            serializer.save(
                artist=artist,
                payment_status='pending',
                approval_status='pending'
            )
        except Artist.DoesNotExist:
            return Response({"error": "Artist profile not found"}, 
                          status=status.HTTP_400_BAD_REQUEST)


class ArtistMySongsView(generics.ListAPIView):
    """Artist can see their own songs"""
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        artist = Artist.objects.get(user=self.request.user)
        return Song.objects.filter(artist=artist).order_by('-uploaded_at')


class SongDownloadView(generics.GenericAPIView):
    """Public download for approved songs"""
    permission_classes = [permissions.AllowAny]

    def get(self, request, song_id):
        song = get_object_or_404(Song, id=song_id, approval_status='approved')
        
        # Increment download count
        song.downloads += 1
        song.save(update_fields=['downloads'])
        
        # Serve file for download
        response = FileResponse(song.audio_file.open('rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{song.title}.mp3"'
        return response