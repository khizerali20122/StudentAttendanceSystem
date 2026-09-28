from django.db import models
from accounts.models import CustomUser


class AdministrativeClass(models.Model):

    name = models.CharField(
        max_length=100
    )

    counselor = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="managed_administrative_classes",
        limit_choices_to={
            "role": "counselor"
        }
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):
        return self.name