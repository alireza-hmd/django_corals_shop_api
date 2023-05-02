from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from drf_spectacular.utils import extend_schema
from . import serializers
from . models import Product, Image, Brand, Category, Comment


class VendorsProductCreateView(APIView):
    @extend_schema(request=serializers.ProductCreateSerializer, responses=serializers.ProductDetailSerializer)
    def post(self, request):
        serializer = serializers.ProductCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        product = Product.objects.create(
            vendor=request.user,
            slug=slugify(data['title']),
            **data,
        )
        context = {'request': request}
        return Response(serializers.ProductListSerializer(instance=product, context=context).data,
                        status=status.HTTP_201_CREATED)


class VendorsProductListView(APIView):
    @extend_schema(responses=serializers.VendorProductListSerializer)
    def get(self, request):
        products = Product.objects.filter(vendor=request.user)
        context = {'request': request}
        serializer = serializers.VendorProductListSerializer(instance=products, context=context, many=True)
        return Response(serializer.data)


class VendorsProductDetailView(APIView):
    @extend_schema(responses=serializers.ProductDetailSerializer)
    def get(self, request, product_slug):
        product = get_object_or_404(Product, vendor=request.user, slug=product_slug)
        serializer = serializers.ProductDetailSerializer(instance=product)
        return Response(serializer.data)

    @extend_schema(request=serializers.ProductCreateSerializer, responses=serializers.ProductListSerializer)
    def put(self, request, product_slug):
        product = get_object_or_404(Product, vendor=request.user, slug=product_slug)
        serializer = serializers.ProductCreateSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        context = {'request': request}
        return Response(serializers.ProductListSerializer(instance=product, context=context).data)

    def delete(self, request, product_slug):
        product = get_object_or_404(Product, vendor=request.user, slug=product_slug)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VendorsImageUploadView(APIView):
    @extend_schema(request=serializers.ImageUploadSerializer, responses=serializers.ImageListSerializer)
    def post(self, request, product_slug):
        serializer = serializers.ImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = get_object_or_404(Product, slug=product_slug)
        image = Image.objects.create(image=serializer.validated_data['image'], product=product)
        context = {'request': request}
        return Response(serializers.ImageListSerializer(instance=image, context=context).data,
                        status=status.HTTP_201_CREATED)


class VendorsImageListView(APIView):
    @extend_schema(responses=serializers.ImageListSerializer)
    def get(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        images = Image.objects.filter(product=product)
        serializer = serializers.ImageListSerializer(instance=images, many=True)
        return Response(serializer.data)


class VendorsImageDetailView(APIView):
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


class ProductListView(APIView):
    @extend_schema(responses=serializers.ProductListSerializer)
    def get(self, request, category_slug=None):
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = Product.objects.filter(category=category)
        else:
            products = Product.objects.all()
        context = {'request': request}
        serializer = serializers.ProductListSerializer(instance=products, context=context, many=True)
        return Response(serializer.data)


class ProductDetailView(APIView):
    @extend_schema(responses=serializers.ProductDetailSerializer)
    def get(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        serializer = serializers.ProductDetailSerializer(instance=product)
        return Response(serializer.data)


class CommentCreateView(APIView):
    @extend_schema(request=serializers.CommentCreateSerializer, responses=serializers.CommentListSerializer)
    def post(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        serializer = serializers.CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        comment = Comment.objects.create(product=product, author=request.user, body=data['body'])
        context = {'request': request}
        return Response(serializers.CommentListSerializer(instance=comment, context=context).data,
                        status=status.HTTP_201_CREATED)


class CommentListView(APIView):
    @extend_schema(responses=serializers.CommentListSerializer)
    def get(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        comments = Comment.objects.filter(product=product)
        serializer = serializers.CommentListSerializer(instance=comments, many=True)
        return Response(serializer.data)


class CommentDeleteView(APIView):
    def delete(self, request, product_slug, comment_id):
        product = get_object_or_404(Product, slug=product_slug)
        comment = get_object_or_404(Comment, product=product, author=request.user)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

