from django.contrib import admin

from .models import UserInfo

admin.site.register(UserInfo)


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('student_id', )

