from django.urls import path

from .views import (
    MarkAttendanceView,
    ScanAttendanceView,
    StudentCourseAttendanceView,
    StudentCoursesView,
    CourseCreateView,
    TestAuthView,
    StudentAttendanceReportView,
    CounselorClassAttendanceReportView,
    AdminAttendanceSummaryView,
    AdminClassAttendanceReportView
    
)



urlpatterns = [

    path(
        "mark/",
        MarkAttendanceView.as_view()
    ),


    path(
        "scan/<int:task_id>/",
        ScanAttendanceView.as_view()
    ),


    path(
        "test-auth/",
        TestAuthView.as_view()
    ),


    path(
        "my-report/",
        StudentAttendanceReportView.as_view()
    ),


    path(
        "class-report/<int:class_id>/",
        CounselorClassAttendanceReportView.as_view()
    ),

    path(
    "admin-summary/",
    AdminAttendanceSummaryView.as_view()
),


path(
    "all-classes-report/",
    AdminClassAttendanceReportView.as_view()
),

path(
    "courses/create/",
    CourseCreateView.as_view(),
    name="course-create"
),

path(
    "student/courses/",
    StudentCoursesView.as_view(),
    name="student-courses"
),

path(
    "student/courses/<int:course_id>/attendance/",
    StudentCourseAttendanceView.as_view(),
    name="student-course-attendance"
),

]