from rest_framework import exceptions, serializers, status

from django.contrib.auth.models import User
from django.db.models import Sum, F
from .models import Product, Stock, Order


class ProductStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'quantity',
            'name',
            'currency',
            'price',
        )

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user

        return super().create(validated_data)


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = (
            'id',
            'quantity',
            'name',
            'currency',
            'price',
        )


class ProductSerializer(serializers.ModelSerializer):
    stocks = serializers.SerializerMethodField()

    def get_stocks(self, obj):
        return obj.stock.quantity

    class Meta:
        model = Product
        fields = (
            'id',
            'quantity',
            'name',
            'currency',
            'price',
            'stocks',
        )


class ProductRevenueSerializer(serializers.ModelSerializer):
    revenue = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    def get_revenue(self, obj):
        order_revenues = obj.order_set.annotate(
            total=Sum(F('quantity') * F('product__price'))
        ).all()
        revenues = 0
        for rev in order_revenues:
            revenues += rev.total

        return f"{obj.currency}{revenues}"

    def get_price(self, obj):
        return f"{obj.currency}{obj.price}"

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'price',
            'revenue'
        )


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'username',
                  'email',
                  'password',
                  'confirm_password']

    def validate(self, attrs: dict):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data: dict) -> User:
        # remove the confirm password
        validated_data.pop('confirm_password')

        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'account')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
            'product',
            'quantity')

    def validate(self, attrs):
        order_quantity = attrs.get('quantity', 0)
        if order_quantity <= 0:
            raise serializers.ValidationError({
                "quantity": "Minimum order quantity is 1!"
            })

        product = attrs.get('product')
        if order_quantity > product.quantity:
            raise serializers.ValidationError({
                "quantity": f"Your order is greater than the available stocks of {order_quantity}!"
            })
        return attrs

    def create(self, validated_data):
        product = validated_data['product']
        quantity = product.stock.quantity if product.stock else 0
        if validated_data['quantity'] > quantity:
            raise exceptions.APIException(
                detail=f"Your order is greater than the available stocks of {quantity}!",
                code=status.HTTP_410_GONE)
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
