"""lengowTestDP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from home import views as home_views
from orders import views as orders_views
from api import urls as api_urls
from rest_framework_swagger import views as swagger_views

docs_urls = swagger_views.get_swagger_view(title='Orders API')

urlpatterns = [
    path('', home_views.index, name='homepage'),
    path('orders/', orders_views.index),
    path('admin/', admin.site.urls),
    path('api/docs/', docs_urls),
    path('api/', include(api_urls)),

]
