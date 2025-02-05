from rest_framework import serializers

from apps.pizza.models import PizzaModel

class PizzaSerializer(serializers.ModelSerializer):

    class Meta:
        model = PizzaModel
        fields = ('id', 'name', 'size', 'price', 'created_at', 'updated_at')


    def validate_price(self, price):
        if price <= 0:
            raise serializers.ValidationError('price must be > than 0')
        return price

    def validate(self, attrs):
        price = attrs.get('price')
        size = attrs.get('size')

        if price == size:
            raise serializers.ValidationError('price cannot = size')
        return attrs


class PizzaPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PizzaModel
        fields = ('photo',)



