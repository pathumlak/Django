from rest_framework import generics
from .models import MenuItem
from .models import Category
from .seralizers import MenuItemSerializer
from .seralizers import CategorySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status 

# class MenuItemsView(generics.ListCreateAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer


# # single Items
# class SingleItemsView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer


# now we look how view on like this
# add here post , get , put , delete
@api_view(['GET', 'POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        serialized_items = MenuItemSerializer(items, many=True)
        return Response(serialized_items.data)
    elif request.method == 'POST':
        serialized_items = MenuItemSerializer(data=request.data)
        serialized_items.is_valid(raise_exception=True)
        serialized_items.save()
        return Response(serialized_items.data, status.HTTP_201_CREATED)

@api_view()
def single_item(request, pk):
    # item = MenuItem.objects.get(pk=pk)
    item = get_object_or_404(MenuItem, pk=pk)
    serialized_item = MenuItemSerializer(item)
    return Response(serialized_item.data)


# this is how view the category
@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serialized_category = CategorySerializer(category)
    return Response(serialized_category.data)

