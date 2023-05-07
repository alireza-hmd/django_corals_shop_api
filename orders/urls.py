from django.urls import path
from . import views

app_name = 'orders'


urlpatterns = [
    path('order/payment/', views.OrderPaymentView.as_view(), name='payment'),
    path('order/<int:order_id>/', views.OrderDetailView.as_view(), name='detail'),
    path('order/', views.OrderCreateView.as_view(), name='create'),
    path('', views.OrderListView.as_view(), name='list'),
]