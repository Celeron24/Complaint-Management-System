from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('complaint/', views.complaint, name='complaint'),
    path('solved/', views.solvedcomplaints, name='solvedcomplaints'),
    path('about/', views.about, name='about'),
]
