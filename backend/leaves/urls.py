from django.urls import path

from .views import (
    ApplyLeaveView,
    MyLeavesView,
    PendingLeavesView,
    ApproveLeaveView,
    RejectLeaveView,
    CancelLeaveView,
    AdminLeaveSummaryView
)

urlpatterns = [

    path(
        "apply/",
        ApplyLeaveView.as_view()
    ),

    path(
        "my-leaves/",
        MyLeavesView.as_view()
    ),

    path(
        "pending/",
        PendingLeavesView.as_view()
    ),

    path(
        "approve/<int:leave_id>/",
        ApproveLeaveView.as_view()
    ),

    path(
        "reject/<int:leave_id>/",
        RejectLeaveView.as_view()
    ),

    path(
    "cancel/<int:leave_id>/",
    CancelLeaveView.as_view()
),

path(
    "admin-summary/",
    AdminLeaveSummaryView.as_view()
),
]