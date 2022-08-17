from django.contrib import admin

from applications.account.models import MyUser

admin.site.register(MyUser)