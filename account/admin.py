from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from account import models

admin.site.unregister(Group)


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "status", "role", "profile_image")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "password1", "password2", "role"),
            },
        ),
    )
    list_display = ("id", "phone_number", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("phone_number", "first_name", "last_name", "email")
    ordering = ("id",)


@admin.register(models.Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ["id", "comment", "employee", "is_solved",]
    list_display_links = list_display
    ordering = ("is_solved",)


@admin.register(models.KeepBusy)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ("id", "programmer", "start_time", "end_time")


@admin.register(models.Board)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(models.Task)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ["id", "name", 'start_date', 'end_date']


