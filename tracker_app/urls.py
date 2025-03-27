from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views

urlpatterns = [
    path('visited_links', views.LinksView.as_view(), name='post_links'),
    path('visited_domains', views.DomainsView.as_view(), name='get_domains'),
]