from django.contrib import admin
from .models import CounselorProfile


@admin.register(CounselorProfile)
class CounselorProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "employee_id",
        "department",
    )