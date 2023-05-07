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


class CartDetailView(APIView):
    @extend_schema(responses=serializers.CartDetailSerializer)
    def get(self, request):
        cart = Cart(request)
        data = {
            'items': cart.get_items(),
            'total_price': cart.get_total_price(),
            'total_price_after_discount': cart.get_total_price_after_discount()
        }
        return Response(serializers.CartDetailSerializer(instance=data).data)


class CartRemoveView(APIView):
    def post(self, request, product_slug):
        cart = Cart(request)
        product = get_object_or_404(Product, slug=product_slug)
        cart.remove(product)
        return Response(status=status.HTTP_204_NO_CONTENT)
