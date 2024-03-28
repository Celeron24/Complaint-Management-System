from django.contrib import admin
from django.urls import path, include

# d0oai32492384h24ui234nij23n4k2jnkjnkjn/
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Comps.urls')),
    path('adminsite/', include('adminsite.urls')),
]
