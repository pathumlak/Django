from rest_framework import serializers
from .models import MenuItem
from decimal import Decimal
from .models import Category


# class MenuItemSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug','title']

# method 1
class MenuItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name='cal_tax')
    # category = CategorySerializer() if you comment this then add depth = 1
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'stock', 'price_after_tax','category', 'category_id']
        depth = 1 #as follows


    def cal_tax(self,product:MenuItem):
        return product.price * Decimal(1.1)


# method 2
# class MenuItemSerializer(serializers.ModelSerializer):
#     stock = serializers.IntegerField(source='inventory')
#     price_after_tax = serializers.SerializerMethodField(method_name='cal_tax')
#     category = serializers.HyperlinkedRelatedField(
#         queryset=Category.objects.all(),
#         view_name='category_detail',
#     )
#     class Meta:
#         model = MenuItem
#         fields = ['id', 'title', 'price', 'stock', 'price_after_tax','category']    

#     def cal_tax(self,product:MenuItem):
#         return product.price * Decimal(1.1)
    
