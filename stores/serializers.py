from rest_framework import serializers
from .models import User, Appointment, Treatment, Prescription


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "role"]


class AppointmentSerializer(serializers.ModelSerializer):

    patient = UserSerializer(read_only=True)
    doctor = UserSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = "__all__"

class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = "__all__"


class PrescriptionSerializer(serializers.ModelSerializer):

    treatments = TreatmentSerializer(many=True, read_only=True)

    treatment_ids = serializers.PrimaryKeyRelatedField(
        queryset=Treatment.objects.all(),
        many=True,
        write_only=True
    )

    class Meta:
        model = Prescription
        fields = ["id", "appointment", "treatments", "treatment_ids", "notes"]

    def validate(self, data):
        request = self.context["request"]
        appointment = data["appointment"]

        if request.user.role != "DOCTOR":
            raise serializers.ValidationError(
                "Only doctors can create prescriptions."
            )

        if appointment.status != "COMPLETED":
            raise serializers.ValidationError(
                "Prescription allowed only for COMPLETED appointments."
            )

        return data

    def create(self, validated_data):
        treatments = validated_data.pop("treatment_ids")

        prescription = Prescription.objects.create(**validated_data)

        prescription.treatments.set(treatments)

        return prescription
