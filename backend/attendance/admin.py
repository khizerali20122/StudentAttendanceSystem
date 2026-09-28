from django.contrib import admin
from .models import AttendanceTask, AttendanceRecord


@admin.register(AttendanceTask)
class AttendanceTaskAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "administrative_class",
        "created_by",
        "method",
        "date",
        "is_active",
    )


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):

    list_display = (
        "task",
        "student",
        "status",
        "check_in_time",
    )