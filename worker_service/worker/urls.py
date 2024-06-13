from django.urls import path
from .views import *
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    # path('info/', StaffInfoView.as_view(), name='staff-detail'),
    path('profile/<int:id>/', StaffDetailAPIView.as_view(), name='staff-detail'),
    path('update/<int:id>/', StaffUpdateAPIView.as_view(), name='staff-update'),
    path('delete/<int:id>/', StaffDeleteAPIView.as_view(), name='staff-delete'),
    path('search/', StaffSearchAPIView.as_view(), name='staff-search'),
    path('logout/', StaffLogoutAPIView.as_view(), name='staff-logout'),
]
