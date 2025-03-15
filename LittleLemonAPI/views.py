from rest_framework import generics
from .models import MenuItem
from .models import Category
from .seralizers import MenuItemSerializer
from .seralizers import CategorySerializer
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status 

# pagination
from django.core.paginator import Paginator, EmptyPage


# this is how render template 
from rest_framework.renderers import TemplateHTMLRenderer


# class MenuItemsView(generics.ListCreateAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer


# # single Items
# class SingleItemsView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer


# now we look how view on like this
# add here post , get , put , delete
# @api_view(['GET', 'POST'])
# def menu_items(request):
#     if request.method == 'GET':
#         items = MenuItem.objects.select_related('category').all()
#         serialized_items = MenuItemSerializer(items, many=True)
#         category_name = request.query_params.get('category')
#         to_price = request.query_params.get('to_price')
#         search = request.query_params.get('search')

#         if category_name:
#             items = items.filter(category__name=category_name)
#         if to_price:
#             items = items.filter(price__lte=to_price)

#         if search:
#             items = items.filter(title__statrswith=search)

#         return Response(serialized_items.data)
#     elif request.method == 'POST':
#         serialized_items = MenuItemSerializer(data=request.data)
#         serialized_items.is_valid(raise_exception=True)
#         serialized_items.save()
#         return Response(serialized_items.data, status.HTTP_201_CREATED)
# @api_view(['GET', 'POST'])
# def menu_items(request):
#     if request.method == 'GET':
#         items = MenuItem.objects.select_related('category').all()
#         serialized_items = MenuItemSerializer(items, many=True)
        
#         # Filter parameters from the query string
#         category_name = request.query_params.get('category')
#         to_price = request.query_params.get('to_price')
#         search = request.query_params.get('search')
#         ordering = request.query_params.get('ordering')


#         # pagination
#         perpage = request.query_params.get('perpage', default=2)
#         page = request.query_params.get('page', default=1)
#         paginator = Paginator(items, per_page=perpage)
#         try:
#             items = paginator.page(number=page)
#         except EmptyPage:
#             items = [paginator.page(1)]

#         if category_name:
#             items = items.filter(category__title=category_name)  # Correct filter for ForeignKey

#         if to_price:
#             items = items.filter(price__lte=to_price)

#         if search:
#             items = items.filter(title__icontains=search) #or contains

#         if ordering:
#             # items = items.order_by(ordering)  or like this 
#             ordering_fields = ordering.split(',')
#             items = items.order_by(*ordering_fields)

#         return Response(serialized_items.data)
    
#     elif request.method == 'POST':
#         serialized_items = MenuItemSerializer(data=request.data)
#         serialized_items.is_valid(raise_exception=True)
#         serialized_items.save()
#         return Response(serialized_items.data, status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def menu_items(request):
    if request.method == 'GET':
        # Filter parameters from the query string
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')

        # Pagination parameters
        perpage = int(request.query_params.get('perpage', 2))
        page = int(request.query_params.get('page', 1))

        # Queryset
        items = MenuItem.objects.select_related('category')

        if category_name:
            items = items.filter(category__title=category_name)
        
        if to_price:
            items = items.filter(price__lte=to_price)
        
        if search:
            items = items.filter(title__icontains=search)
        
        if ordering:
            ordering_fields = ordering.split(',')
            items = items.order_by(*ordering_fields)

        # Pagination
        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(page)
        except EmptyPage:
            items = []

        # Serialize the paginated items
        serialized_items = MenuItemSerializer(items, many=True)
        return Response(serialized_items.data)
    
    elif request.method == 'POST':
        serialized_items = MenuItemSerializer(data=request.data)
        serialized_items.is_valid(raise_exception=True)
        serialized_items.save()
        return Response(serialized_items.data, status=status.HTTP_201_CREATED)

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


# this is how render html template
@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def menu(request):
    items = MenuItem.objects.select_related('category').all()
    serialized_items = MenuItemSerializer(items, many=True)
    return Response({'items': serialized_items.data}, template_name='menu-items.html')


# from rest_framework import viewsets
# # class based view
# class MenuItemsViewSet(viewsets.ModelViewSet):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer
#     ordering_fields=['price','inventory']
#     search_fields=['title']
