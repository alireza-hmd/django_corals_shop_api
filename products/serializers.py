from rest_framework import serializers
from django.core.validators import FileExtensionValidator
from .models import Product


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'category', 'brand', 'price', 'volume', 'description')


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('vendor', 'title', 'brand', 'price', 'available')


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField(
        validators=[FileExtensionValidator(['jpeg', 'jpg', 'png'])]
    )
    product_slug = serializers.SlugField()


class ImageListSerializer(serializers.Serializer):
    image_url = serializers.CharField()
    product_slug = serializers.SlugField()


