from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from drf_spectacular.utils import extend_schema
from django.conf import settings
import redis
from . import serializers
from . models import Product, Image, Brand, Category, Comment

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


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
        if request.GET.get('available') == '1':
            products = products.filter(available=True)
        if request.GET.get('brands'):
            brands = request.GET.get('brands')
            brands = brands.split(',')
            products = products.filter(brand__name__in=brands)
        if request.GET.get('most_viewed'):
            count = int(request.GET.get('most_viewed'))
            if count == 0:
                product_ranking = r.zrevrange('product_ranking', 0, -1)
            else:
                product_ranking = r.zrevrange('product_ranking', 0, -1)[:count]
            product_ranking_ids = [int(id) for id in product_ranking]
            products = list(Product.objects.filter(id__in=product_ranking_ids))
            products.sort(key=lambda x: product_ranking_ids.index(x.id))
        context = {'request': request}
        serializer = serializers.ProductListSerializer(instance=products, context=context, many=True)
        return Response(serializer.data)


class ProductDetailView(APIView):
    @extend_schema(responses=serializers.ProductDetailSerializer)
    def get(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        r.incr(f'product:{product.id}:views')
        r.zincrby('product_ranking', 1, product.id)
        context = {'request': request}
        serializer = serializers.ProductDetailSerializer(instance=product, context=context)
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
        comment = get_object_or_404(Comment, product=product, id=comment_id, author=request.user)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SearchView(APIView):
    @extend_schema(responses=serializers.ProductListSerializer)
    def get(self, request):
        query = request.GET.get('q')
        search_vector = SearchVector('title', 'category__title', 'brand__name', 'description')
        search_query = SearchQuery(query)
        results = Product.objects.annotate(
            search=search_vector, rank=SearchRank(search_vector, search_query)
        ).filter(search=search_query).order_by('-rank')
        context = {'request': request}
        serializer = serializers.ProductListSerializer(instance=results, context=context, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentLikeView(APIView):
    def get(self, request, product_slug, comment_id):
        product = get_object_or_404(Product, slug=product_slug)
        comment = get_object_or_404(Comment, product=product, id=comment_id)
        comment.likes_number += 1
        comment.save()
        return Response(status=status.HTTP_200_OK)


class CommentDislikeView(APIView):
    def get(self, request, product_slug, comment_id):
        product = get_object_or_404(Product, slug=product_slug)
        comment = get_object_or_404(Comment, product=product, id=comment_id)
        comment.dislikes_number += 1
        comment.save()
        return Response(status=status.HTTP_200_OK)
