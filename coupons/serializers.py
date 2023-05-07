from rest_framework import serializers


class CouponApplySerializer(serializers.Serializer):
    code = serializers.CharField(max_length=50)

