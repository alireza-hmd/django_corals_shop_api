from django.urls import path
from . import views

app_name = 'orders'


urlpatterns = [
    path('order/', views.OrderCreateView.as_view(), name='create'),
    path('order/<int:order_id>/', views.OrderDetailView.as_view(), name='detail'),
    path('', views.OrderListView.as_view(), name='list'),
]