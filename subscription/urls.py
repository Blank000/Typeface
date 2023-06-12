from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView
)

app_urlpatterns = [
    # to create access token
    path('user/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # to refresh access token
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Create User by Admin
    path('user/signup/', views.UserCreateAPIView.as_view(), name='create_user'),
    # Update User type vy Admin
    path('user/update_user/', views.UserUpdateView.as_view(), name='update_user_type'),
    # Buy Package
    path('package/create/', views.UserCreateTeamPackageView.as_view(), name='buy_package'),
    # After Pay for  Package
    path('package/payment/update', views.PackagePaymentUpdateView.as_view(), name='package_payment'),
    # Mock product 
    path('typeface/generate_content/', views.TypefaceContentCreateView.as_view(), name='typeface_generate_content'),
    # List user usage for any active Package
    path('package/fetch_usage_details/', views.FetchPackageUsageDetailsView.as_view(), name='fetch_package_usage_details'),
]

