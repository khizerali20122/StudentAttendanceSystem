from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.models import CustomUser
from administrative_classes.models import AdministrativeClass

from .models import LeaveRequest

from .serializers import LeaveRequestSerializer

from students.models import StudentProfile



# ==========================
# Student Apply Leave
# ==========================

class ApplyLeaveView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def post(self, request):

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


        leave = LeaveRequest.objects.create(

            student=student,

            reason=request.data.get("reason"),

            start_date=request.data.get("start_date"),

            end_date=request.data.get("end_date")

        )


        serializer = LeaveRequestSerializer(
            leave
        )


        return Response(
            serializer.data,
            status=201
        )





# ==========================
# Student View Leaves
# ==========================

class MyLeavesView(APIView):

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
                    "error":"Student profile not found"
                },
                status=404
            )


        leaves = LeaveRequest.objects.filter(
            student=student
        )


        serializer = LeaveRequestSerializer(
            leaves,
            many=True
        )


        return Response(
            serializer.data
        )
    # ==========================
# Counselor View Pending Leaves
# ==========================

class PendingLeavesView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(self, request):

        if request.user.role != "counselor":

            return Response(
                {
                    "error": "Only counselors can view leaves"
                },
                status=403
            )


        classes = AdministrativeClass.objects.filter(
            counselor=request.user
        )


        leaves = LeaveRequest.objects.filter(
            student__administrative_class__in=classes,
            status="pending"
        )


        serializer = LeaveRequestSerializer(
            leaves,
            many=True
        )


        return Response(
            serializer.data
        )



# ==========================
# Approve Leave
# ==========================

class ApproveLeaveView(APIView):
    
    permission_classes = [
        IsAuthenticated
    ]


    def post(self, request, leave_id):

        if request.user.role != "counselor":

            return Response(
                {
                    "error": "Only counselors can approve leaves"
                },
                status=403
            )


        try:

            leave = LeaveRequest.objects.get(
                id=leave_id
            )

        except LeaveRequest.DoesNotExist:

            return Response(
                {
                    "error": "Leave not found"
                },
                status=404
            )


        # Check counselor owns student's class

        if leave.student.administrative_class.counselor != request.user:

            return Response(
                {
                    "error": "You cannot approve this student's leave"
                },
                status=403
            )


        if leave.status != "pending":

            return Response(
                {
                    "error": "Only pending leaves can be approved"
                },
                status=400
            )


        leave.status = "approved"

        leave.approved_by = request.user

        leave.save()


        return Response(
            {
                "message": "Leave approved successfully"
            }
        )

# ==========================
# Reject Leave
# ==========================

class RejectLeaveView(APIView):
    
    permission_classes = [
        IsAuthenticated
    ]


    def post(self, request, leave_id):

        if request.user.role != "counselor":

            return Response(
                {
                    "error": "Only counselors can reject leaves"
                },
                status=403
            )


        try:

            leave = LeaveRequest.objects.get(
                id=leave_id
            )

        except LeaveRequest.DoesNotExist:

            return Response(
                {
                    "error": "Leave not found"
                },
                status=404
            )


        # Security check

        if leave.student.administrative_class.counselor != request.user:

            return Response(
                {
                    "error": "You cannot reject this student's leave"
                },
                status=403
            )


        if leave.status != "pending":

            return Response(
                {
                    "error": "Only pending leaves can be rejected"
                },
                status=400
            )


        leave.status = "rejected"

        leave.approved_by = request.user

        leave.save()


        return Response(
            {
                "message": "Leave rejected successfully"
            }
        )
    # ==========================
# Student Cancel Leave
# ==========================

class CancelLeaveView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def delete(self, request, leave_id):

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


        try:

            leave = LeaveRequest.objects.get(
                id=leave_id,
                student=student
            )

        except LeaveRequest.DoesNotExist:

            return Response(
                {
                    "error": "Leave not found"
                },
                status=404
            )


        if leave.status != "pending":

            return Response(
                {
                    "error": "Only pending leaves can be cancelled"
                },
                status=400
            )


        leave.status = "cancelled"

        leave.save()


        return Response(
            {
                "message": "Leave cancelled successfully"
            }
        )

    # ==========================
# Admin Leave Summary
# ==========================

class AdminLeaveSummaryView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(self, request):

        if request.user.role != "admin":

            return Response(
                {
                    "error": "Only admins can view leave statistics"
                },
                status=403
            )


        total = LeaveRequest.objects.count()


        pending = LeaveRequest.objects.filter(
            status="pending"
        ).count()


        approved = LeaveRequest.objects.filter(
            status="approved"
        ).count()


        rejected = LeaveRequest.objects.filter(
            status="rejected"
        ).count()


        cancelled = LeaveRequest.objects.filter(
            status="cancelled"
        ).count()


        return Response(
            {
                "total_requests": total,
                "pending": pending,
                "approved": approved,
                "rejected": rejected,
                "cancelled": cancelled
            }
        )