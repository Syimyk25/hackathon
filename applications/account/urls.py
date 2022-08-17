from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from applications.account.views import *

urlpatterns = [
    path('register/', RegisterApiView.as_view()),
    path('active/<uuid:activation_code>/', ActivationView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('forgot_password/', ForgotPasswordView.as_view()),
    path('password_recovery/', ForgotPasswordComplete.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path('auth/', include('rest_framework_social_oauth2.urls')),
]