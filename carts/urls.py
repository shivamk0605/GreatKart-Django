from django.urls import path
from .import views
urlpatterns = [
    path('', views.cart,name='cart'),
    path('addcart/<int:product_id>/',views.addCart,name='addcart'),
    path('reduceCart/<int:product_id>/',views.reduceCart,name='reduceCart'),
    path('removeCartItem/<int:product_id>/',views.removeCartItem,name='removeCartItem'),
    
]