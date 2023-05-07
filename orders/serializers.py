from rest_framework import serializers
from .models import Order


class OrderInputSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    address = serializers.CharField(max_length=250)
    postal_code = serializers.CharField(max_length=20)
    city = serializers.CharField(max_length=100)


class OrderOutputSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField('get_items')
    total_cost = serializers.SerializerMethodField('get_total_cost')

    class Meta:
        model = Order
        fields = ('customer', 'first_name', 'last_name', 'email', 'address', 'postal_code',
                  'city', 'created_at', 'paid', 'items', 'total_cost')

    def get_items(self, order):
        items = list()
        for item in order.items.all():
            items.append({'item': str(item), 'cost': item.get_cost()})
        return items

    def get_total_cost(self, order):
        total_cost = 0
        for item in order.items.all():
            total_cost += item.get_cost()
        return str(total_cost)

