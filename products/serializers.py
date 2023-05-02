from rest_framework import serializers
from django.core.validators import FileExtensionValidator
from .models import Product, Brand, Category, Image


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

class ImageListSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField('get_image_url')
    class Meta:
        model = Image
        fields = ('id', 'product', 'image_url')

    def get_image_url(self, image):
        return image.image.url


class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

