from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from products.models import Product
from . import serializers
from .cart import Cart


class CartAddView(APIView):
    @extend_schema(request=serializers.CartAddSerializer, responses=serializers.CartListSerializer)
    def post(self, request, product_slug):
        serializer = serializers.CartAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        cart = Cart(request)
        product = get_object_or_404(Product, slug=product_slug)
        cart.add(product, quantity=data['quantity'], override_quantity=data['override_quantity'])
        return Response(serializers.CartListSerializer(instance=cart.get_item(product)).data)


class CartListView(APIView):
    @extend_schema(responses=serializers.CartListSerializer)
    def get(self, request):
        cart = Cart(request)
        return Response(serializers.CartListSerializer(instance=cart.get_items(), many=True).data)


class CartRemoveView(APIView):
    def post(self, request, product_slug):
        cart = Cart(request)
        product = get_object_or_404(Product, slug=product_slug)
        cart.remove(product)
        return Response(status=status.HTTP_204_NO_CONTENT)
