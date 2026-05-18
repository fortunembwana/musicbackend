from django.urls import path
from .views import SongUploadView, ArtistMySongsView, SongDownloadView

urlpatterns = [
    path('upload/', SongUploadView.as_view(), name='song-upload'),
    path('my-songs/', ArtistMySongsView.as_view(), name='my-songs'),
    path('download/<int:song_id>/', SongDownloadView.as_view(), name='song-download'),
]