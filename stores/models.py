from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    ROLE_CHOICES = (
        ("DOCTOR", "Doctor"),
        ("PATIENT", "Patient"),
        ("ADMIN", "Admin"),
    )

    name = models.CharField(max_length=200)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Appointment(models.Model):

    STATUS_CHOICES = (
        ("SCHEDULED", "Scheduled"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    )

    patient = models.ForeignKey(
        User,
        related_name="patient_appointments",
        on_delete=models.CASCADE
    )

    doctor = models.ForeignKey(
        User,
        related_name="doctor_appointments",
        on_delete=models.CASCADE
    )

    appointment_date = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="SCHEDULED"
    )

    def __str__(self):
        return f"{self.patient.username} → {self.doctor.username}"



class Treatment(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class Prescription(models.Model):
    appointment = models.ForeignKey(
        Appointment,
        related_name="prescriptions",
        on_delete=models.CASCADE
    )

    treatments = models.ManyToManyField(Treatment)

    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Prescription for {self.appointment.patient.username}"

