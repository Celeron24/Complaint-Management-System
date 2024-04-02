from django.urls import path
from . import views
from .views import ComplaintDetailView

urlpatterns = [
    path('signin/', views.signin, name='signIn'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admcomplaint/<int:pk>/', ComplaintDetailView.as_view(), name='complaint_detail'),
    path('add_dept/', views.add_department, name='add_department'),
    path('add_user/', views.add_user, name='add-user')
]
