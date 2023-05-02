from rest_framework import serializers
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from .models import Product, Brand, Category, Image


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


class ProductListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField('get_url')

    class Meta:
        model = Product
        fields = ('vendor', 'title', 'brand', 'price', 'available', 'url')

    def get_url(self, product):
        request = self.context.get('request')
        path = reverse('products:customer_detail', args=(product.slug,))
        return request.build_absolute_uri(path)
