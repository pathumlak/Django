from django.urls import path
from . import views


urlpatterns = [
    # path('menu-items', views.MenuItemsView.as_view()),   
    # path('menu-items/<int:pk>', views.SingleItemsView.as_view())
    path('menu-items', views.menu_items),
    path('menu-items/<int:pk>', views.single_item),


    # cateogory routes method 1
    path('category/<int:pk>', views.category_detail),
    
]