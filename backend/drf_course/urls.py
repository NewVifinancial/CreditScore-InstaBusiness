"""drf_course URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
from core import views as core_views
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from loans import views as loans_views



router = routers.DefaultRouter()
# router.register(r'item', ecommerce_views.ItemViewSet, basename='item')
# router.register(r'order', ecommerce_views.OrderViewSet, basename='order')

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    # path('contact/', core_views.ContactAPIView.as_view()),
    path('transactions/', loans_views.TransactionsAPIView.as_view()),    
    path('transactions/<id_num>/', loans_views.transactionRetrieveAPIview),    

    path('calculations/', loans_views.CalculationAPIView.as_view()),   
    path('calculations/<id_num>/', loans_views.calculationRetrieveAPIview),   

    path('creditscore/', loans_views.CreditScoreAPIView.as_view()),    
    path('creditscore/<id_num>/', loans_views.creditScoreRetrieveAPIview),    

    path('api-token-auth/', obtain_auth_token),
]
