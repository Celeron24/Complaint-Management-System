from django.urls import path
from . import views
from .views import ComplaintDetailView

urlpatterns = [
    path('adminsite/choose/', views.signin, name='signIn'),
    path('adminsite/admin_login/', views.admin_login, name='admin_login'),
    path('adminsite/admin_logout/', views.admin_logout, name='admin_logout'),
    path('adminsite/dashboard/', views.dashboard, name='dashboard'),
    path('adminsite/admcomplaint/<int:pk>/', ComplaintDetailView.as_view(), name='complaint_detail'),
    path('adminsite/add_dept/', views.add_department, name='add_department'),
    path('adminsite/user_management/', views.user_management, name='user_management'),
    path('adminsite/add_user/', views.add_user, name='add_user'),
]
