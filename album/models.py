from django.db import models
from user_management.models import BaseModel
from artists.models import Artist
from songs.models import Song   


# Create your models here.
class Album(BaseModel):
    album_id = models.AutoField(primary_key=True)
    album_name = models.CharField(max_length=255)
    artist = models.ForeignKey('artists.Artist', on_delete=models.CASCADE, related_name='albums')
    cover_image = models.ImageField(upload_to='albums/covers/')
    number_of_songs = models.PositiveIntegerField(default=0)
    release_date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.album_name

class AlbumSong(models.Model):
    album_song_id = models.AutoField(primary_key=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='album_songs')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='song_albums')

    class Meta:
        unique_together = ('album', 'song')