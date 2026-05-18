from django.db import models
from songs.models import Song

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('airtel_money', 'Airtel Money'),
        ('mpamba', 'Mpamba'),
        ('bank', 'Bank Transfer'),
    ]
    STATUS = [('pending', 'Pending'), ('completed', 'Completed'), ('rejected', 'Rejected')]

    songs = models.OneToOneField(Song, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    transaction_reference = models.CharField(max_length=255)
    proof_image = models.ImageField(upload_to='payments/')
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"self.song.title - {self.transaction_reference}"
