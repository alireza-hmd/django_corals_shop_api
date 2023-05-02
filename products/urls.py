from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('create/', views.ProductCreateView.as_view(), name='create'),
    path('brands/', views.BrandListView.as_view(), name='brands'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('product/<slug:product_slug>/', views.ProductDetailView.as_view(), name='detail'),
    path('', views.ProductListView.as_view(), name='list'),
]
