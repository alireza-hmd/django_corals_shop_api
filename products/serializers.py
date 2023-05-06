from rest_framework import serializers
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from django.conf import settings
import redis
from .models import Product, Brand, Category, Image, Comment

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'category', 'brand', 'price', 'volume', 'description')


class VendorProductListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField('get_url')
    class Meta:
        model = Product
        fields = ('vendor', 'title', 'brand', 'price', 'available', 'url')

    def get_url(self, product):
        request = self.context.get('request')
        path = reverse('products:vendor_detail', args=(product.slug,))
        return request.build_absolute_uri(path)


class ProductDetailSerializer(serializers.ModelSerializer):
    views = serializers.SerializerMethodField('get_views')

    class Meta:
        model = Product
        fields = ('id', 'title', 'slug', 'price', 'volume', 'description', 'available',
                  'created_at', 'updated_at', 'vendor', 'category', 'brand', 'product_images',
                  'product_comments', 'views')

    def get_views(self, product):
        return r.get(f'product:{product.id}:views')


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


class ProductListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField('get_url')

    class Meta:
        model = Product
        fields = ('vendor', 'title', 'brand', 'price', 'available', 'url')

    def get_url(self, product):
        request = self.context.get('request')
        path = reverse('products:customer_detail', args=(product.slug,))
        return request.build_absolute_uri(path)


class CommentCreateSerializer(serializers.Serializer):
    body = serializers.CharField()


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
