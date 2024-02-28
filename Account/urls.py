from django.urls import path
from . import views 

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('staff/register/', views.RegisterStaffView.as_view(), name='staff_auth_register'),
    path('access-staff', views.access_staff, name="access-staff" ),
    path('webcustomer/register/', views.WebCustomerCreateView.as_view(), name='webcustomer_auth_register'),
    path('webcustomer/approve/<int:_id>/', views.approve_web_customer, name='approve_web_customer'),
    path('webcustomer/approve/list/', views.retrieve_approved_customers, name='approved_web_customer'),
    path('webcustomer/not-approve/list/', views.retrieve_not_approved_customers, name='not-approve_web_customer'),

    path('staff/profile/', views.get_profiles, name='staff-profile'),
    path('staff/profile/<int:pk>/', views.get_profile, name='staff-profiles'),
    path('update/staff/profile/<int:pk>/', views.update_profile, name='update-staff'),

    path('webcustomer/profile/access/', views.WebCustomerListView.as_view(), name='webcustomer_list_all'),
    path('webcustomer/profile/<int:id>/', views.WebCustomerEdit.as_view(), name='webcuster_list'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot-password'),
]