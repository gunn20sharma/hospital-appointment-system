from rest_framework.permissions import BasePermission

class IsAppointmentOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.user.role == "DOCTOR":
            return obj.doctor == request.user

        if request.user.role == "PATIENT":
            return obj.patient == request.user

        return False
