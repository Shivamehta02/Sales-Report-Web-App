"""reports_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import login_view,logout_view, register_view



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('sales.urls',namespace= 'sales')),
    path('reports/',include('reports.urls',namespace= 'reports')),
    path('products/',include('products.urls',namespace= 'products')),
    path('my_profile/',include('profiles.urls',namespace= 'profiles')),#since it only has one view
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('register/',register_view, name= 'register'),
    path('chatbot/', include('chatbot.urls')),
    
    
    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Report Admin"
admin.site.site_title = "Report Admin"
admin.site.index_title = "Welcome to Report Admin settings"