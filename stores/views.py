from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Appointment, Prescription, Treatment
from .serializers import (
    AppointmentSerializer,
    PrescriptionSerializer,
    TreatmentSerializer,
)
from .permissions import IsAppointmentOwner


class AppointmentListView(generics.ListCreateAPIView):

    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["doctor", "status", "appointment_date"]

    def get_queryset(self):
        user = self.request.user

        if user.role == "PATIENT":
            return Appointment.objects.filter(patient=user)
        if user.role == "DOCTOR":
            return Appointment.objects.filter(doctor=user)

        return Appointment.objects.all()


class AppointmentRetrieveUpdateDestroyView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsAppointmentOwner]

class PrescriptionCreateView(generics.CreateAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]


class PrescriptionListView(generics.ListAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["appointment"]


class TreatmentListView(generics.ListAPIView):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer
    permission_classes = [IsAuthenticated]
