from rest_framework import serializers


class CartAddSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(required=False)
    override_quantity = serializers.BooleanField(default=False)


class CartListSerializer(serializers.Serializer):
    product = serializers.SlugField()
    quantity = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=14, decimal_places=2)
