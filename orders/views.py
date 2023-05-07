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
from products.recommender import Recommender

class OrderCreateView(APIView):
    @extend_schema(request=serializers.OrderInputSerializer, responses=serializers.OrderListSerializer)
    def post(self, request):
        serializer = serializers.OrderInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        cart = Cart(request)
        if cart.coupon:
            order = Order.objects.create(customer=request.user, coupon=cart.coupon,
                                         discount=cart.coupon.discount, **data)
        else:
            order = Order.objects.create(customer=request.user, **data)
        for item in cart:
            product = get_object_or_404(Product, slug=item['product'])
            OrderItem.objects.create(order=order, product=product, price=item['price'], quantity=item['quantity'])
        cart.clear()
        context = {'request': request}
        return Response(serializers.OrderListSerializer(instance=order, context=context).data,
                        status=status.HTTP_201_CREATED)


class OrderListView(APIView):

    @extend_schema(responses=serializers.OrderListSerializer)
    def get(self, request):
        orders = Order.objects.filter(customer=request.user)
        if request.GET.get('paid') == '1':
            orders = orders.filter(paid=True)
        elif request.GET.get('paid') == '0':
            orders = orders.filter(paid=False)
        context = {'request': request}
        serializer = serializers.OrderListSerializer(instance=orders, context=context, many=True)
        return Response(serializer.data)


class OrderDetailView(APIView):
    @extend_schema(responses=serializers.OrderDetailSerializer)
    def get(self, request, order_id):
        order = get_object_or_404(Order, customer=request.user, id=order_id)
        serializer = serializers.OrderDetailSerializer(instance=order)
        return Response(serializer.data)

    def delete(self, request, order_id):
        order = get_object_or_404(Order, customer=request.user, id=order_id)
        if not order.paid:
            order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderPaymentView(APIView):
    @extend_schema(request=serializers.OrderPaymentSerializer, responses=serializers.OrderListSerializer)
    def post(self, request):
        serializer = serializers.OrderPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_id = serializer.validated_data['order_id']
        order = get_object_or_404(Order, customer=request.user, id=order_id)
        order.paid = True
        order.save()
        products = [item.product for item in order.items.all()]
        r = Recommender()
        r.products_bought(products)
        return Response()

