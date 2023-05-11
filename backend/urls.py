
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = router.urls

urlpatterns = [
     path('polls/', include('polls.urls')),
     path('loans/', include('loans.urls')),
     path('admin/', admin.site.urls),
]

