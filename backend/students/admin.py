from django.contrib import admin
from .models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "student_id",
        "major",
        "administrative_class",
    )

    search_fields = (
        "student_id",
        "user__username",
    )