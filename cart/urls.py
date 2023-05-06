from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartListView.as_view(), name='list'),
    path('add/<product_slug>/', views.CartAddView.as_view(), name='add'),
    path('remove/<product_slug>/', views.CartRemoveView.as_view(), name='remove'),
]
