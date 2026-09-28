from math import radians, sin, cos, sqrt, atan2
from administrative_classes.models import AdministrativeClass

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.models import CustomUser
from administrative_classes.models import AdministrativeClass
from .models import Course, AttendanceRecord


from .models import AttendanceTask, AttendanceRecord
from .serializers import AttendanceRecordSerializer
from .serializers import StudentCourseSerializer
from .serializers import CourseCreateSerializer

from students.models import StudentProfile



# ==========================
# GPS Distance Calculator
# ==========================

def calculate_distance(lat1, lon1, lat2, lon2):

    earth_radius = 6371000  # meters


    lat1 = radians(float(lat1))
    lon1 = radians(float(lon1))

    lat2 = radians(float(lat2))
    lon2 = radians(float(lon2))


    dlat = lat2 - lat1
    dlon = lon2 - lon1


    a = (
        sin(dlat / 2) ** 2
        +
        cos(lat1)
        *
        cos(lat2)
        *
        sin(dlon / 2) ** 2
    )


    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )


    return earth_radius * c





# ==========================
# Test JWT Authentication
# ==========================

class TestAuthView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(self, request):

        return Response({

            "message": "JWT authentication working",

            "username": request.user.username,

            "user_id": request.user.id

        })






# ==========================
# Manual Attendance API
# ==========================

class MarkAttendanceView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def post(self, request):

        task_id = request.data.get(
            "task_id"
        )


        if not task_id:

            return Response(
                {
                    "error": "task_id is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        try:

            task = AttendanceTask.objects.get(
                id=task_id,
                is_active=True
            )


        except AttendanceTask.DoesNotExist:

            return Response(
                {
                    "error": "Attendance task not found"
                },
                status=404
            )



        try:

            student = StudentProfile.objects.get(
                user=request.user
            )


        except StudentProfile.DoesNotExist:

            return Response(
                {
                    "error": "Student profile not found"
                },
                status=404
            )



        record, created = AttendanceRecord.objects.get_or_create(

            task=task,

            student=student,

            defaults={
                "status": "present"
            }

        )


        if not created:

            return Response(
                {
                    "message": "Attendance already marked"
                },
                status=400
            )


        serializer = AttendanceRecordSerializer(
            record
        )


        return Response(
            serializer.data,
            status=201
        )






# ==========================
# QR + GPS Attendance API
# ==========================

class ScanAttendanceView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def post(self, request, task_id):


        try:

            task = AttendanceTask.objects.get(
                id=task_id,
                is_active=True
            )


        except AttendanceTask.DoesNotExist:

            return Response(
                {
                    "error": "Attendance task not found"
                },
                status=404
            )



        try:

            student = StudentProfile.objects.get(
                user=request.user
            )


        except StudentProfile.DoesNotExist:

            return Response(
                {
                    "error": "Student profile not found"
                },
                status=404
            )



        latitude = request.data.get(
            "latitude"
        )


        longitude = request.data.get(
            "longitude"
        )



        # GPS Validation

        if (
            task.classroom_latitude
            and task.classroom_longitude
        ):


            if not latitude or not longitude:

                return Response(
                    {
                        "error": "GPS location required"
                    },
                    status=400
                )



            distance = calculate_distance(

                latitude,

                longitude,

                task.classroom_latitude,

                task.classroom_longitude

            )


            if distance > task.allowed_radius:

                return Response(
                    {
                        "error": "You are outside classroom range",

                        "distance": round(
                            distance,
                            2
                        ),

                        "allowed_radius": task.allowed_radius
                    },

                    status=400
                )



        record, created = AttendanceRecord.objects.get_or_create(

            task=task,

            student=student,


            defaults={

                "status": "present",

                "latitude": latitude,

                "longitude": longitude

            }

        )


        if not created:

            return Response(
                {
                    "message": "Attendance already marked",

                    "student": student.id,

                    "task": task.id
                },

                status=400
            )



        serializer = AttendanceRecordSerializer(
            record
        )


        return Response(
            {
                "message": "Attendance marked successfully",

                "attendance": serializer.data
            },

            status=201
        )






# ==========================
# Student Attendance Report
# ==========================

class StudentAttendanceReportView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(self, request):


        try:

            student = StudentProfile.objects.get(
                user=request.user
            )


        except StudentProfile.DoesNotExist:

            return Response(
                {
                    "error": "Student profile not found"
                },
                status=404
            )



        records = AttendanceRecord.objects.filter(
            student=student
        )



        total_classes = records.count()


        present = records.filter(
            status="present"
        ).count()


        absent = records.filter(
            status="absent"
        ).count()



        percentage = 0


        if total_classes > 0:

            percentage = round(
                (present / total_classes) * 100,
                2
            )



        serializer = AttendanceRecordSerializer(
            records,
            many=True
        )



        return Response({

            "student": request.user.username,

            "total_classes": total_classes,

            "present": present,

            "absent": absent,

            "attendance_percentage": percentage,

            "records": serializer.data

        })

    # ==========================
# Counselor Class Attendance Report
# ==========================

class CounselorClassAttendanceReportView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(self, request, class_id):

        try:

            administrative_class = AdministrativeClass.objects.get(
                id=class_id,
                counselor=request.user
            )


        except AdministrativeClass.DoesNotExist:

            return Response(
                {
                    "error": "Class not found or you are not assigned as counselor"
                },
                status=404
            )


        students = administrative_class.students.all()


        total_students = students.count()


        student_reports = []


        total_present = 0

        total_absent = 0



        for student in students:


            records = AttendanceRecord.objects.filter(
                student=student
            )


            total_classes = records.count()


            present = records.filter(
                status="present"
            ).count()


            absent = records.filter(
                status="absent"
            ).count()



            total_present += present

            total_absent += absent



            percentage = 0


            if total_classes > 0:

                percentage = round(
                    (present / total_classes) * 100,
                    2
                )


            student_reports.append({

                "student_id": student.student_id,

                "student": student.user.username,

                "total_classes": total_classes,

                "present": present,

                "absent": absent,

                "attendance_percentage": percentage

            })



        total_classes_count = (
            total_present + total_absent
        )


        overall_percentage = 0


        if total_classes_count > 0:

            overall_percentage = round(
                (total_present / total_classes_count) * 100,
                2
            )


        return Response({

            "class": administrative_class.name,

            "total_students": total_students,

            "total_present": total_present,

            "total_absent": total_absent,

            "attendance_percentage": overall_percentage,

            "students": student_reports

        })

    # ==========================
# Admin Attendance Summary
# ==========================

class AdminAttendanceSummaryView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(self, request):

        # Check admin role

        if request.user.role != "admin":

            return Response(
                {
                    "error": "Admin access required"
                },
                status=403
            )


        total_students = StudentProfile.objects.count()


        total_classes = AttendanceTask.objects.count()


        total_records = AttendanceRecord.objects.count()


        present = AttendanceRecord.objects.filter(
            status="present"
        ).count()


        absent = AttendanceRecord.objects.filter(
            status="absent"
        ).count()


        percentage = 0


        if total_records > 0:

            percentage = round(
                (present / total_records) * 100,
                2
            )


        return Response({

            "total_students": total_students,

            "total_classes": total_classes,

            "total_attendance_records": total_records,

            "present": present,

            "absent": absent,

            "overall_attendance_percentage": percentage

        })


class StudentCoursesView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):

        student = StudentProfile.objects.get(
            user=request.user
        )

        courses = Course.objects.filter(
            administrative_class=student.administrative_class
        ).order_by("name")

        serializer = StudentCourseSerializer(
            courses,
            many=True
        )

        return Response(serializer.data)

# =========================================================
# COURSE CREATION
# Admin + Counselor
# =========================================================

class CourseCreateView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        # -------------------------------------------------
        # Check role
        # -------------------------------------------------

        if request.user.role not in [
            "admin",
            "counselor"
        ]:

            return Response(
                {
                    "detail": (
                        "Only admin or counselor "
                        "can create courses."
                    )
                },
                status=status.HTTP_403_FORBIDDEN
            )


        # -------------------------------------------------
        # Validate request data
        # -------------------------------------------------

        serializer = CourseCreateSerializer(
            data=request.data
        )


        if not serializer.is_valid():

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


        administrative_class = serializer.validated_data[
            "administrative_class"
        ]


        # -------------------------------------------------
        # Counselor permission
        # -------------------------------------------------

        if request.user.role == "counselor":

            is_assigned = AdministrativeClass.objects.filter(
                id=administrative_class.id,
                counselor=request.user
            ).exists()


            if not is_assigned:

                return Response(
                    {
                        "detail": (
                            "You can only create courses "
                            "for your assigned class."
                        )
                    },
                    status=status.HTTP_403_FORBIDDEN
                )


        # -------------------------------------------------
        # Prevent duplicate course names in same batch
        # -------------------------------------------------

        course_name = serializer.validated_data[
            "name"
        ]


        existing_course = Course.objects.filter(
            administrative_class=administrative_class,
            name__iexact=course_name
        ).first()


        if existing_course:

            return Response(
                {
                    "detail": (
                        "A course with this name "
                        "already exists for this class."
                    ),
                    "course_id": existing_course.id
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        # -------------------------------------------------
        # Prevent duplicate course code in same batch
        # -------------------------------------------------

        course_code = serializer.validated_data.get(
            "code"
        )


        if course_code:

            existing_code = Course.objects.filter(
                administrative_class=administrative_class,
                code__iexact=course_code
            ).first()


            if existing_code:

                return Response(
                    {
                        "detail": (
                            "A course with this code "
                            "already exists for this class."
                        ),
                        "course_id": existing_code.id
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )


        # -------------------------------------------------
        # Create course
        # -------------------------------------------------

        course = serializer.save()


        # -------------------------------------------------
        # Return created course
        # -------------------------------------------------

        return Response(
            {
                "message": "Course created successfully.",

                "course": CourseCreateSerializer(
                    course
                ).data
            },

            status=status.HTTP_201_CREATED
        )
    
class StudentCourseAttendanceView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):

        student = StudentProfile.objects.get(
            user=request.user
        )

        try:

            course = Course.objects.get(
                id=course_id,
                administrative_class=student.administrative_class
            )

        except Course.DoesNotExist:

            return Response(
                {
                    "detail": "Course not found."
                },
                status=404
            )


        tasks = course.attendance_tasks.all()


        records = AttendanceRecord.objects.filter(
            student=student,
            task__in=tasks
        ).select_related(
            "task"
        ).order_by(
            "task__date"
        )


        total_classes = tasks.count()

        present = records.filter(
            status="present"
        ).count()

        absent = records.filter(
            status="absent"
        ).count()


        if total_classes > 0:

            percentage = round(
                (present / total_classes) * 100,
                2
            )

        else:

            percentage = 0


        attendance_records = []


        for record in records:

            attendance_records.append(
                {
                    "id": record.id,
                    "date": record.task.date,
                    "status": record.status,
                    "task_title": record.task.title
                }
            )


        return Response(
            {
                "course": {
                    "id": course.id,
                    "name": course.name,
                    "code": course.code
                },

                "total_classes": total_classes,

                "present": present,

                "absent": absent,

                "attendance_percentage": percentage,

                "records": attendance_records
            }
        )   
    # ==========================
# Admin Class Attendance Report
# ==========================

class AdminClassAttendanceReportView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(self, request):


        if request.user.role != "admin":

            return Response(
                {
                    "error": "Admin access required"
                },
                status=403
            )


        classes = AdministrativeClass.objects.all()


        reports = []


        for cls in classes:


            students = cls.students.all()


            records = AttendanceRecord.objects.filter(
                student__in=students
            )


            total = records.count()


            present = records.filter(
                status="present"
            ).count()


            percentage = 0


            if total > 0:

                percentage = round(
                    (present / total) * 100,
                    2
                )


            reports.append({

                "class": cls.name,

                "students": students.count(),

                "total_records": total,

                "present": present,

                "attendance_percentage": percentage

            })


        return Response({

            "classes": reports

        })

        