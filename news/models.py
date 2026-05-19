from django.db import models
from user_management.models import BaseModel

class Category(BaseModel):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    
class News(BaseModel):
    news_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='news')
    
    def __str__(self):
        return self.title

class NewsImage(models.Model):
    news_image_id = models.AutoField(primary_key=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='news/images/')

    def __str__(self):
        return f"Image for {self.news.title}"
