from rest_framework import serializers
from .models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='slug', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'category',
                  'price', 'description', 'image']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
