from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('register.urls')),
    path('patient/', include('patient.urls')),
    path('controll/', include('controll.urls')),
]
