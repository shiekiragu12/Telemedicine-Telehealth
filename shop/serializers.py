from rest_framework import serializers

from .models import Product, ProductType, Category, Payment, Order, OrderItem, PrescriptionOrder, ProductImage
from account.publicserializers import PubUserSerializer


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        categories = validated_data.pop('categories')
        tags = validated_data.pop('tags')
        product = Product.objects.create(**validated_data)
        product.categories.set(categories)
        product.tags.set(tags)
        product.save()
        images = self.initial_data.getlist('images', None)
        if len(images) > 0:
            productImages = [ProductImage(product=product, image=image) for image in images]
            ProductImage.objects.bulk_create(productImages)
        return product


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'price', 'quantity', 'created_on', 'updated_on']

    def to_representation(self, instance):
        self.fields['product'] = ProductSerializer(many=False)
        return super(OrderItemSerializer, self).to_representation(instance)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'paid', 'amount', 'created_on', 'order_items', 'updated_on']

    def to_representation(self, instance):
        self.fields['user'] = PubUserSerializer(many=False)
        self.fields['order_items'] = OrderItemSerializer(many=True)
        return super(OrderSerializer, self).to_representation(instance)


class PrescriptionOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionOrder
        fields = ['id', 'patient', 'facility', 'prescription', 'amount', 'notes', 'status', 'paid']
