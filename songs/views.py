from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Song
from .serializers import SongSerializer
from artists.models import Artist

class SongUploadView(generics.CreateAPIView):
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
            return Response({"error": "Artist profile not found"}, status=status.HTTP_400_BAD_REQUEST)


class ArtistMySongsView(generics.ListAPIView):
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        artist = Artist.objects.get(user=self.request.user)
        return Song.objects.filter(artist=artist).order_by('-uploaded_at')