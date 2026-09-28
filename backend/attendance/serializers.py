from rest_framework import serializers

from .models import AttendanceRecord
from .models import Course
from administrative_classes.models import AdministrativeClass


class StudentCourseSerializer(serializers.ModelSerializer):

    class_name = serializers.CharField(
        source="administrative_class.name",
        read_only=True
    )

    class Meta:
        model = Course

        fields = [
            "id",
            "name",
            "code",
            "class_name",
        ]


class AttendanceRecordSerializer(serializers.ModelSerializer):

    task_title = serializers.CharField(
        source="task.title",
        read_only=True
    )

    student_name = serializers.CharField(
        source="student.user.username",
        read_only=True
    )

    class Meta:
        model = AttendanceRecord

        fields = [
            "id",
            "task",
            "task_title",
            "student",
            "student_name",
            "status",
            "check_in_time",
            "latitude",
            "longitude",
        ]


# =========================================================
# COURSE CREATION SERIALIZER
# =========================================================

class CourseCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course

        fields = [
            "id",
            "name",
            "code",
            "administrative_class",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_name(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Course name is required."
            )

        return value

    def validate_code(self, value):

        if value is None:
            return value

        value = value.strip()

        if not value:
            return None

        return value

    def validate_administrative_class(self, value):

        if not isinstance(
            value,
            AdministrativeClass
        ):
            raise serializers.ValidationError(
                "Invalid administrative class."
            )

        return value