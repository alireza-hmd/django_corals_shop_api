from django.urls import path, include
from . import views

app_name = 'products'

urlpatterns = [
    # Vendor URLs
    path('vendors/products/', include([
        path('create/', views.VendorsProductCreateView.as_view(), name='vendor_create'),
        path('<slug:product_slug>/', views.VendorsProductDetailView.as_view(), name='vendor_detail'),
        path('<slug:product_slug>/image_uplaod/', views.VendorsImageUploadView.as_view(), name='vendor_image_upload'),
        path('<slug:product_slug>/image_list/', views.VendorsImageListView.as_view(), name='vendor_image_list'),
        path('<slug:product_slug>/<int:image_id>/', views.VendorsImageDetailView.as_view(), name='vendor_image_detail'),
        path('', views.VendorsProductListView.as_view(), name='vendor_list'),
    ])),

    # Customer URLs
    path('products/', include([
        path('<slug:product_slug>/comments/', include([
            path('', views.CommentListView.as_view(), name='comment_list'),
            path('create/', views.CommentCreateView.as_view(), name='comment_create'),
            path('<int:comment_id>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
        ])),
        path('<slug:category_slug>/', views.ProductListView.as_view(), name='customer_category_list'),
        path('product/<slug:product_slug>/', views.ProductDetailView.as_view(), name='customer_detail'),
        path('', views.ProductListView.as_view(), name='customer_list'),

    ])),
]
