from rest_framework import serializers


class CartAddSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(required=False)
    override_quantity = serializers.BooleanField(default=False)


class CartListSerializer(serializers.Serializer):
    product = serializers.SlugField()
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=14, decimal_places=2)


class CartDetailSerializer(serializers.Serializer):
    items = CartListSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=14, decimal_places=2)
    total_price_after_discount = serializers.DecimalField(max_digits=14, decimal_places=2)