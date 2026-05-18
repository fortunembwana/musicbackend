from django.urls import path
from .views import (
    SongUploadView, 
    ArtistMySongsView, 
    SongDownloadView, 
    SongStreamView
)

urlpatterns = [
    path('upload/', SongUploadView.as_view(), name='song-upload'),
    path('my-songs/', ArtistMySongsView.as_view(), name='my-songs'),
    path('download/<int:song_id>/', SongDownloadView.as_view(), name='song-download'),
    path('stream/<int:song_id>/', SongStreamView.as_view(), name='song-stream'),
]