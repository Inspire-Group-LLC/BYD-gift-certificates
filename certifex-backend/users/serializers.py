from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    is_superuser = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ["full_name", "phone_number", "username", "password", "is_superuser"]

    def create(self, validated_data):
        # Extract is_superuser from the validated data
        is_superuser = validated_data.pop('is_superuser', False)

        # Create the user with the remaining data
        user = User.objects.create_user(is_superuser=is_superuser, **validated_data)
        return user