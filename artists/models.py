from django.db import models
from django.contrib.auth.models import User

class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stage_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='artists/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
                                      
    def __str__(self):
        return self.stage_name
