from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    model = CustomUser

    list_display = (
        "username",
        "email",
        "role",
        "is_staff",
        "is_active",
    )

    list_display_links = (
        "username",
    )

    fieldsets = (
        (None, {
            "fields": (
                "username",
                "password",
            )
        }),

        ("Personal Information", {
            "fields": (
                "first_name",
                "last_name",
                "email",
            )
        }),

        ("Role Information", {
            "fields": (
                "role",
                "phone",
                "is_active_account",
            )
        }),

        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),

        ("Important Dates", {
            "fields": (
                "last_login",
                "date_joined",
            )
        }),
    )