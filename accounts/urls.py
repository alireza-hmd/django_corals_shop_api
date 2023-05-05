from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from . import views

urlpatterns = [
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/forgot_password/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    # jwt authentication
    path('auth/', include([
        path('login/', TokenObtainPairView.as_view(), name='login'),
        path('refresh/', TokenRefreshView.as_view(), name='refresh'),
        path('verify/', TokenVerifyView.as_view(), name='verify'),
    ]), name='jwt')
]
