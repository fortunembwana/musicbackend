
from django.db import models
from artists.models import Artist
from user_management.models import BaseModel


class Category(BaseModel):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Song(BaseModel):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid')
    ]

    APPROVAL_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]

    song_id = models.AutoField(primary_key=True)

    artist = models.ForeignKey(
        'artists.Artist',
        on_delete=models.CASCADE,
        related_name='songs'
    )

    album = models.ForeignKey(
        'album.Album',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='songs'
    )

    title = models.CharField(max_length=255)

    genre = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    cover_image = models.ImageField(
        upload_to='songs/covers/'
    )

    audio_file = models.FileField(
        upload_to='songs/audio/'
    )

    description = models.TextField(blank=True)

    year_released = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    file_type = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    file_size = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    duration = models.DurationField(
        null=True,
        blank=True
    )

    bitrate = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    quality = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    waveform = models.JSONField(
        blank=True,
        null=True
    )

    plays = models.IntegerField(default=0)

    download_count = models.IntegerField(default=0)

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='pending'
    )

    approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_STATUS,
        default='pending'
    )

    streams = models.IntegerField(default=0)

    downloads = models.IntegerField(default=0)

    def __str__(self):
        return self.title
# from django.db import models
# from artists.models import Artist
# from user_management.models import BaseModel


# class Category(BaseModel):
#     category_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=30, unique=True)

#     def __str__(self):
#         return self.name
    

# class Song(BaseModel):
#     PAYMENT_STATUS = [('pending', 'Pending'), ('paid', 'Paid')]
#     APPROVAL_STATUS = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]

#     song_id = models.AutoField(primary_key=True)

#     artist = models.ForeignKey(
#         'artists.Artist',
#         on_delete=models.CASCADE,
#         related_name='songs'
#     )

#     album = models.ForeignKey(
#         'album.Album',
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name='songs'
#     )

#     title = models.CharField(max_length=255)
#     cover_image = models.ImageField(upload_to='songs/covers/')
#     description = models.TextField(blank=True)

#     genre = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
#     year_realesed = models.PositiveIntegerField(null=True, blank=True) 
#     audio_file = models.FileField(upload_to='songs/audio/')
#     file_type = models.CharField(max_length=50, blank=True, null=True)  # New field to store file type (e.g., "mp3", "wav")
#     file_size = models.PositiveIntegerField(null=True, blank=True)  # New field to store file size in bytes
#     duration = models.DurationField(null=True, blank=True)  # New field to store song duration
#     bitrate = models.PositiveIntegerField(null=True, blank=True)  # New field to store bitrate in kbps
#     quality = models.CharField(max_length=50, blank=True, null=True)  # New field to store quality description (e.g., "320kbps", "Lossless")
#     waveform = models.JSONField(blank=True, null=True)  # New field to store waveform data as JSON
#     plays = models.IntegerField(default=0)  # New field to track number of plays
#     download_count = models.IntegerField(default=0)  # New field to track number of downloads
#     payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
#     approval_status = models.CharField(max_length=20, choices=APPROVAL_STATUS, default='pending')
    
#     streams = models.IntegerField(default=0)
#     downloads = models.IntegerField(default=0)          # ← New field

#     def __str__(self):
#         return self.title


# class Payment(BaseModel):
#     PAYMENT_METHODS = [
#         ('airtel_money', 'Airtel Money'),
#         ('mpamba', 'Mpamba'),
#         ('bank', 'Bank Transfer'),
#         ('cash', 'Cash'),
#     ]
#     STATUS = [('pending', 'Pending'), ('completed', 'Completed'), ('rejected', 'Rejected')]

#     payment_id = models.AutoField(primary_key=True)
#     song = models.OneToOneField(Song, on_delete=models.CASCADE)
#     payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
#     transaction_reference = models.CharField(max_length=255, unique=True, blank=True, null=True)
#     proof_image = models.ImageField(upload_to='payments/', blank=True, null=True)
#     status = models.CharField(max_length=20, choices=STATUS, default='pending')
#     amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

#     def __str__(self):
#         return f"{self.song.title} - {self.transaction_reference}"
