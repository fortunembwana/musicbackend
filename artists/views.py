from rest_framework import generics, permissions

from .models import Artist
from .serializers import (
    ArtistSerializer,
    ArtistListSerializer,
    ArtistDetailSerializer
)


class ArtistCreateView(generics.CreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [permissions.IsAuthenticated]


class ArtistListView(generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistListSerializer
    permission_classes = [permissions.AllowAny]


class ArtistDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "artist_id"