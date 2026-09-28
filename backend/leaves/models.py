from django.db import models

from accounts.models import CustomUser
from students.models import StudentProfile



class LeaveRequest(models.Model):

    STATUS_CHOICES = (

        ("pending", "Pending"),

        ("approved", "Approved"),

        ("rejected", "Rejected"),

        ("cancelled", "Cancelled"),

    )


    student = models.ForeignKey(

        StudentProfile,

        on_delete=models.CASCADE,

        related_name="leave_requests"

    )


    reason = models.TextField()



    start_date = models.DateField()



    end_date = models.DateField()



    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default="pending"

    )



    approved_by = models.ForeignKey(

        CustomUser,

        on_delete=models.SET_NULL,

        null=True,

        blank=True,

        related_name="approved_leaves"

    )



    created_at = models.DateTimeField(

        auto_now_add=True

    )



    updated_at = models.DateTimeField(

        auto_now=True

    )



    def __str__(self):

        return f"{self.student} - {self.status}"