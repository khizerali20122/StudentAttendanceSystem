from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from accounts.views import CustomTokenObtainPairView


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),


    # JWT Login
    path(
        "api/token/",
        CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair"
    ),


    # JWT Refresh
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),


    # Attendance APIs
    path(
        "api/attendance/",
        include("attendance.urls")
    ),


    # Leave APIs
    path(
        "api/leaves/",
        include("leaves.urls")
    ),

]