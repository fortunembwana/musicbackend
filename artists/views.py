# from rest_framework import generics, status
# from rest_framework.response import Response
# from django.contrib.auth.models import User
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# from .models import Artist
# from .serializers import ArtistRegisterSerializer   


# class ArtistRegisterView(generics.CreateAPIView):
#     serializer_class = ArtistRegisterSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         artist = serializer.save()
        
#         return Response({
#             "message": "Artist registered successfully",
#             "artist": {
#                 "stage_name": artist.stage_name,
#                 "username": artist.user.username
#             }
#         }, status=status.HTTP_201_CREATED)


# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token['username'] = user.username
        
#         # Safely add stage_name if artist profile exists
#         if hasattr(user, 'artist'):
#             token['stage_name'] = user.artist.stage_name
            
#         return token


# class ArtistLoginView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer