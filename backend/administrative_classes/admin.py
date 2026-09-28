from django.contrib import admin
from .models import AdministrativeClass


@admin.register(AdministrativeClass)
class AdministrativeClassAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "counselor",
        "created_at",
    )

    search_fields = (
        "name",
        "counselor__username",
    )