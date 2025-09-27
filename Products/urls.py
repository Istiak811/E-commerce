from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("category_products/<slug:category_slug>/", views.category_products, name='category_products'),
    path("product/<slug:product_slug>/", views.product_detail, name='product'),
    path("product/<slug:product_slug>/review/", views.submit_review, name='review'),

    path('shop-left-sidebar.html', views.shop_left_sidebar, name='shop_left_sidebar'),
]