# from django.db import models
# from django.contrib.auth.models import User
# from user_management.models import BaseModel

# class Artist(BaseModel):
#     artist_id = models.AutoField(primary_key=True)
#     full_name = models.CharField(max_length=100, blank=True, null=True)
#     lastname = models.CharField(max_length=30, blank=True, null=True)
#     stage_name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     phone_number = models.CharField(max_length=20, blank=True, null=True)
#     bio = models.TextField(blank=True, null=True)
#     profile_image = models.ImageField(upload_to='artists_profiles/', blank=True, null=True)
#     is_verified = models.BooleanField(default=False)
       
#     def __str__(self):
#         return self.stage_name

from django.db import models
from django.contrib.auth.models import User
from user_management.models import BaseModel


class Artist(BaseModel):
    artist_id = models.AutoField(primary_key=True)

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='artist_profile'
    )

    stage_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(
        upload_to='artists_profiles/',
        blank=True,
        null=True
    )

    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.stage_name