from django.urls import path, include
from . import views

app_name = 'products'

urlpatterns = [
    path('create/', views.ProductCreateView.as_view(), name='create'),
    path('brands/', views.BrandListView.as_view(), name='brands'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('product/', include([
        path('<slug:product_slug>/', views.ProductDetailView.as_view(), name='detail'),
        path('<slug:product_slug>/image_uplaod/', views.ImageUploadView.as_view(), name='image_upload'),
        path('<slug:product_slug>/image_list/', views.ImageListView.as_view(), name='image_list'),
        path('<slug:product_slug>/<int:image_id>/', views.ImageDetailView.as_view(), name='image_detail'),
    ])),
    path('', views.ProductListView.as_view(), name='list'),
]
