from django.urls import path
from . import views
from .views import ViewComplaint

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('complaint/', views.complaint, name='complaint'),
    path('solved/', views.solvedcomplaints, name='solvedcomplaints'),
    path('about/', views.about, name='about'),
    path('view_complaint/<int:pk>/', ViewComplaint.as_view(), name='view_complaint'),
    path('search/', views.your_search_view, name='search'),
]


# path('new/', ComplaintCreateView.as_view(), name='complaint-create'),
#     path('<int:pk>/', complaint_detail, name='complaint-detail'),
#     path('<int:pk>/update/', ComplaintUpdateView.as_view(), name='complaint-update'),
#     path('<int:pk>/delete/', ComplaintDeleteView.as_view(), name='complaint-delete'),
#     path('<int:pk>/status_change/', status_change, name='status-change'),
