"""
URL configuration for tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from prometheus_client import make_wsgi_app
from django.views.decorators.csrf import csrf_exempt
from django.contrib import admin
from djoser import views as djoser_views
from djoser.views import TokenDestroyView, TokenCreateView
from django.urls import path, include, re_path
from .yasg import urlpatterns as doc_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tracker_app.urls')),
    path('metrics/', csrf_exempt(make_wsgi_app())),
    # path('api/auth/users/', djoser_views.UserViewSet.as_view({'post': 'create'}), name='user-create'),
    re_path(r'^auth/token/login/$', TokenCreateView.as_view(), name='token-login'),
    re_path(r'^auth/token/logout/$', TokenDestroyView.as_view(), name='token-logout'),
    path('', include('users.urls')),
]

urlpatterns += doc_urls
