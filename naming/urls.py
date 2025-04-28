from django.urls import path
from . import views

urlpatterns = [
    path('', views.pokemon_list, name='pokemon_list'),
    path('cart/add/<int:pokemon_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('checkout/', views.checkout, name='checkout'),
    path('compare/', views.compare_pokemons, name='compare_pokemons'),  # 新增
    path('pokemon/<int:pk>/', views.pokemon_detail, name='pokemon_detail'),
    path('pokemon/<int:pk>/order/', views.order_pokemon, name='order_pokemon'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('register/', views.register, name='register'),
]