from django.urls import path
from users.views import CustomUserRegistrationView

urlpatterns = [
    path('auth/register/', CustomUserRegistrationView.as_view({'post': 'create'}), name='user-registration'),
]