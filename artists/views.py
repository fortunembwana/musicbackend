from rest_framework import generics, status
from rest_framework.response import Response
from .models import Artist
from .serializers import ArtistSerializer, ArtistListSerializer, ArtistDetailSerializer 


class ArtistCreateView(generics.CreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        artist = serializer.save()
        
        return Response({
            "message": "Artist created successfully",
            "artist": {
                "artist_id": artist.artist_id,
                "stage_name": artist.stage_name,
                "email": artist.email
            }
        }, status=status.HTTP_201_CREATED)




class ArtistListView(generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistListSerializer
    

class ArtistDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistDetailSerializer






