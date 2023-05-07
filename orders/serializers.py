from rest_framework import serializers
from .models import Order


class OrderInputSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    address = serializers.CharField(max_length=250)
    postal_code = serializers.CharField(max_length=20)
    city = serializers.CharField(max_length=100)


class OrderListSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField('get_items')
    total_cost_before_discount = serializers.SerializerMethodField('get_total_cost_before_discount')
    total_cost = serializers.SerializerMethodField('get_total_cost')
    url = serializers.SerializerMethodField('get_url')
    class Meta:
        model = Order
        fields = ('id', 'customer', 'paid', 'items', 'total_cost_before_discount', 'total_cost', 'url')

    def get_items(self, order):
        items = list()
        for item in order.items.all():
            items.append({'item': str(item), 'cost': item.get_cost()})
        return items

    def get_total_cost_before_discount(self, order):
        return order.get_total_cost_before_discount()

    def get_total_cost(self, order):
        return order.get_total_cost()

    def get_url(self, order):
        request = self.context.get('request')
        path = order.get_absolute_url()
        return request.build_absolute_uri(path)


class OrderDetailSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField('get_items')
    total_cost_before_discount = serializers.SerializerMethodField('get_total_cost_before_discount')
    total_cost = serializers.SerializerMethodField('get_total_cost')

    class Meta:
        model = Order
        fields = ('id', 'customer', 'first_name', 'last_name', 'email', 'address', 'postal_code',
                  'city', 'created_at', 'paid', 'items', 'total_cost_before_discount', 'total_cost')

    def get_items(self, order):
        items = list()
        for item in order.items.all():
            items.append({'item': str(item), 'cost': item.get_cost()})
        return items

    def get_total_cost_before_discount(self, order):
        return order.get_total_cost_before_discount()

    def get_total_cost(self, order):
        return order.get_total_cost()


class OrderPaymentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()


