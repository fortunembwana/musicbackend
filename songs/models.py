from django.db import models
from artists.models import Artist

class Song(models.Model):
    PAYMENT_STATUS = [('pending', 'Pending'), ('paid', 'Paid')]
    APPROVAL_STATUS = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='songs/covers/')
    audio_file = models.FileField(upload_to='songs/audio/')
    description = models.TextField(blank=True)
    
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    approval_status = models.CharField(max_length=20, choices=APPROVAL_STATUS, default='pending')
    
    streams = models.IntegerField(default=0)
    downloads = models.IntegerField(default=0)          # ← New field
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title