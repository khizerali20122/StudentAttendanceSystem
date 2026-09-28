import qrcode

from io import BytesIO

from django.db import models
from django.core.files import File

from accounts.models import CustomUser
from students.models import StudentProfile
from administrative_classes.models import AdministrativeClass



class AttendanceTask(models.Model):

    title = models.CharField(
        max_length=200
    )


    administrative_class = models.ForeignKey(
        AdministrativeClass,
        on_delete=models.CASCADE
    )


    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )


    method = models.CharField(
        max_length=20
    )


    date = models.DateField()


    start_time = models.TimeField()


    end_time = models.TimeField()


    is_active = models.BooleanField(
        default=True
    )


    qr_code = models.ImageField(
        upload_to="attendance_qr/",
        null=True,
        blank=True
    )

    course = models.ForeignKey(
    "attendance.Course",
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="attendance_tasks"
)


    # GPS classroom location
    classroom_latitude = models.FloatField(
        null=True,
        blank=True
    )


    classroom_longitude = models.FloatField(
        null=True,
        blank=True
    )


    # Allowed distance in meters
    allowed_radius = models.IntegerField(
        default=100
    )


    def save(self, *args, **kwargs):

        # Save first to generate ID
        super().save(*args, **kwargs)


        # Generate QR only once
        if not self.qr_code:

            qr_data = (
                f"http://127.0.0.1:8000/api/attendance/scan/{self.id}/"
            )


            qr = qrcode.make(qr_data)


            buffer = BytesIO()


            qr.save(
                buffer,
                format="PNG"
            )


            file_name = (
                f"attendance_task_{self.id}.png"
            )


            self.qr_code.save(
                file_name,
                File(
                    buffer
                ),
                save=False
            )


            super().save(
                update_fields=[
                    "qr_code"
                ]
            )


    def __str__(self):

        return self.title

class Course(models.Model):
    name = models.CharField(max_length=150)

    code = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    administrative_class = models.ForeignKey(
        "administrative_classes.AdministrativeClass",
        on_delete=models.CASCADE,
        related_name="courses"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        if self.code:
            return f"{self.name} ({self.code})"

        return self.name



class AttendanceRecord(models.Model):

    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
    )


    task = models.ForeignKey(
        AttendanceTask,
        on_delete=models.CASCADE,
        related_name="records"
    )


    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="attendance_records"
    )


    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES
    )


    check_in_time = models.DateTimeField(
        auto_now_add=True
    )


    # Student GPS location
    latitude = models.FloatField(
        null=True,
        blank=True
    )


    longitude = models.FloatField(
        null=True,
        blank=True
    )


    class Meta:

        unique_together = (
            'task',
            'student'
        )


    def __str__(self):

        return f"{self.student} - {self.status}"

        