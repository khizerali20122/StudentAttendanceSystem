from django.db import models
from accounts.models import CustomUser
from administrative_classes.models import AdministrativeClass


class StudentProfile(models.Model):

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={
            "role": "student"
        }
    )

    student_id = models.CharField(
        max_length=50,
        unique=True
    )

    major = models.CharField(
        max_length=100
    )

    administrative_class = models.ForeignKey(
        AdministrativeClass,
        on_delete=models.CASCADE,
        related_name="students"
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.username