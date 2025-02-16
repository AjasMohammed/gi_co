from .models import UserData
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['name', 'email', 'age']

    def validate_age(self, value):
        """
        Validates the age.
            - validates if the age field is in the required range.
        """
        if value <= 0 or value > 120:
            raise serializers.ValidationError('Age should be between 0 and 120!')

        return value