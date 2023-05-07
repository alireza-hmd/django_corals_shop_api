from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from cart.cart import Cart
from products.models import Product
from .models import Order, OrderItem
from . import serializers


class OrderCreateView(APIView):
    @extend_schema(request=serializers.OrderInputSerializer, responses=serializers.OrderOutputSerializer)
    def post(self, request):
        serializer = serializers.OrderInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        order = Order.objects.create(customer=request.user, **data)
        cart = Cart(request)
        for item in cart:
            product = get_object_or_404(Product, slug=item['product'])
            OrderItem.objects.create(order=order, product=product, price=item['price'], quantity=item['quantity'])
        cart.clear()
        return Response(serializers.OrderOutputSerializer(instance=order).data, status=status.HTTP_201_CREATED)


class OrderListView(APIView):

    @extend_schema(responses=serializers.OrderOutputSerializer)
    def get(self, request):
        orders = Order.objects.filter(customer=request.user)
        if request.GET.get('paid') == '1':
            orders = orders.filter(paid=True)
        elif request.GET.get('paid') == '0':
            orders = orders.filter(paid=False)
        serializer = serializers.OrderOutputSerializer(instance=orders, many=True)
        return Response(serializer.data)


class OrderDetailView(APIView):
    @extend_schema(responses=serializers.OrderOutputSerializer)
    def get(self, request, order_id):
        order = get_object_or_404(Order, customer=request.user, id=order_id)
        serializer = serializers.OrderOutputSerializer(instance=order)
        return Response(serializer.data)

    def delete(self, request, order_id):
        order = get_object_or_404(Order, customer=request.user, id=order_id)
        if not order.paid:
            order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderPaymentView(APIView):
    @extend_schema(request=serializers.OrderPaymentSerializer, responses=serializers.OrderPaidSerializers)
    def post(self, request):
        serializer = serializers.OrderPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        order = get_object_or_404(Order, customer=request.user, id=data['order_id'])
        total_price = sum(item.get_cost() for item in order.items.all())
        if total_price == data['total_price']:
            order.paid = True
            order.save()
        return Response(serializers.OrderPaidSerializer(instance=order).data)

