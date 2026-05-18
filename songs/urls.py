from django.urls import path
from .views import SongUploadView, ArtistMySongsView

urlpatterns = [
    path('upload/', SongUploadView.as_view(), name='song-upload'),
    path('my-songs/', ArtistMySongsView.as_view(), name='my-songs'),
]