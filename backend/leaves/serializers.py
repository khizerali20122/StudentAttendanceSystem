from rest_framework import serializers

from .models import LeaveRequest



class LeaveRequestSerializer(serializers.ModelSerializer):

    student = serializers.CharField(
        source="student.user.username",
        read_only=True
    )


    approved_by = serializers.CharField(
        source="approved_by.username",
        read_only=True
    )


    class Meta:

        model = LeaveRequest

        fields = [

            "id",

            "student",

            "reason",

            "start_date",

            "end_date",

            "status",

            "approved_by",

            "created_at",

            "updated_at"

        ]