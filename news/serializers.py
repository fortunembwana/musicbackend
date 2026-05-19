from rest_framework import serializers
from .models import News, NewsImage

class NewsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsImage
        fields = ['news_image_id', 'image']

class NewsCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = News
        fields = ['news_id', 'title', 'content', 'category', 'images','created_at', 'added_by',]

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        news = super().create(validated_data)
        for image in images:
            NewsImage.objects.create(news=news, image=image)
        return news