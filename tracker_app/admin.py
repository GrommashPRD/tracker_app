from django.contrib import admin
from django.contrib.auth.models import User

from tracker_app.models import UserDomainsHistory

# Register your models here.

admin.site.register(UserDomainsHistory)