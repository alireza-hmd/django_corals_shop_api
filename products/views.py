from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from drf_spectacular.utils import extend_schema
from . import serializers
from . models import Product, Image, Brand, Category


class ProductCreateView(APIView):
    @extend_schema(request=serializers.ProductCreateSerializer, responses=serializers.ProductDetailSerializer)
    def post(self, request):
        serializer = serializers.ProductCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        product = Product.objects.create(
            vendor=request.user,
            title=data['title'],
            slug=slugify(data['title']),
            category=data['category'],
            brand=data['brand'],
            price=data['price'],
            volume=data['volume'],
            description=data['description'],
        )
        context = {'request': request}
        return Response(serializers.ProductDetailSerializer(instance=product, context=context).data,
                        status=status.HTTP_201_CREATED)


class ProductListView(APIView):
    @extend_schema(responses=serializers.ProductListSerializer)
    def get(self, request):
        products = Product.objects.filter(vendor=request.user)
        serializer = serializers.ProductListSerializer(instance=products, many=True)
        return Response(serializer.data)


class ProductDetailView(APIView):
    @extend_schema(responses=serializers.ProductDetailSerializer)
    def get(self, request, product_slug):
        product = get_object_or_404(Product, vendor=request.user, slug=product_slug)
        serializer = serializers.ProductDetailSerializer(instance=product)
        return Response(serializer.data)

    def delete(self, request, product_slug):
        product = get_object_or_404(Product, vendor=request.user, slug=product_slug)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BrandListView(APIView):
    @extend_schema(responses=serializers.BrandListSerializer)
    def get(self, request):
        brands = Brand.objects.all()
        serializer = serializers.BrandListSerializer(instance=brands, many=True)
        return Response(serializer.data)


class CategoryListView(APIView):
    @extend_schema(responses=serializers.CategoryListSerializer)
    def get(self, request):
        categories = Category.objects.all()
        serializer = serializers.CategoryListSerializer(instance=categories, many=True)
        return Response(serializer.data)


class ImageUploadView(APIView):
    @extend_schema(request=serializers.ImageUploadSerializer, responses=serializers.ImageListSerializer)
    def post(self, request, product_slug):
        serializer = serializers.ImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = get_object_or_404(Product, slug=product_slug)
        image = Image.objects.create(image=serializer.validated_data['image'], product=product)
        context = {'request': request}
        return Response(serializers.ImageListSerializer(instance=image, context=context).data,
                        status=status.HTTP_201_CREATED)


class ImageListView(APIView):
    @extend_schema(responses=serializers.ImageListSerializer)
    def get(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        images = Image.objects.filter(product=product)
        serializer = serializers.ImageListSerializer(instance=images, many=True)
        return Response(serializer.data)


class ImageDetailView(APIView):
    @extend_schema(responses=serializers.ImageListSerializer)
    def get(self, request, product_slug, image_id):
        product = get_object_or_404(Product, slug=product_slug)
        image = get_object_or_404(Image, product=product, id=image_id)
        serializer = serializers.ImageListSerializer(instance=image)
        return Response(serializer.data)

    def delete(self, request, product_slug, image_id):
        product = get_object_or_404(Product, slug=product_slug)
        image = get_object_or_404(Image, product=product, id=image_id)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

