from django.contrib import admin
from .models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.admin import UserAdmin


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    # inlines = (TwitchAccountInline, TwitterAccountInline)


admin.site.register(User, MyUserAdmin)
