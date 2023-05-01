from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from . import serializers
from . models import Product, Image


class ProductView(APIView):
    def post(self, request):
        serializer = serializers.ProductCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        product = Product.objects.create(
            vendor=request.user,
            title=data['title'],
            category=data['category'],
            brand=data['brand'],
            price=data['price'],
            volume=data['volume'],
            description=data['description'],
        )
        context = {'request': request}
        return Response(serializers.ProductDetailSerializer(product, context).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        products = Product.objects.filter(vendor=request.user)
        serializer = serializers.ProductListSerializer(instance=products, many=True)
        return Response(serializer.data)


class ProductDetailView(APIView):
    def get(self, request, product_slug):
        product = get_object_or_404(Product, vendor=request.user, slug=product_slug)
        serializer = serializers.ProductDetailSerializer(instance=product)
        return Response(serializer.data)

    def delete(self, request, product_slug):
        product = get_object_or_404(Product, vendor=request.user, slug=product_slug)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

