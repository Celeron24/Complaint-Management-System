from django.contrib import messages
from django.shortcuts import redirect
from django.urls import path
from . import views
from .views import ComplaintDetailView


def custom_staff_member_required(view_func):
    """
    Decorator that redirects staff members to another page if they are not authorized.
    """
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            messages.warning(request, 'You are not allowed to access this, Unauthorized access')
            return redirect('home')  # Replace 'another_page' with the name of your desired page
    return _wrapped_view


urlpatterns = [
    path('', views.signin, name='signIn'),
    path('adminsite/admin_login/', views.admin_login, name='admin_login'),
    path('adminsite/admin_logout/', custom_staff_member_required(views.admin_logout), name='admin_logout'),
    path('adminsite/dashboard/', custom_staff_member_required(views.dashboard), name='dashboard'),
    path('adminsite/admcomplaint/<int:pk>/', ComplaintDetailView.as_view(), name='complaint_detail'),
    path('adminsite/add_dept/', custom_staff_member_required(views.add_department), name='add_department'),
    path('adminsite/user_management/', custom_staff_member_required(views.user_management), name='user_management'),
    path('adminsite/add_user/', custom_staff_member_required(views.add_user), name='add_user'),
]
