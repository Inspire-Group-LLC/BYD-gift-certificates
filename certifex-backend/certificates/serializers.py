from rest_framework import serializers
from certificates.models import Certificate
from users.serializers import UserSerializer
from users.models import User
from django.db import transaction
from django.core.exceptions import MultipleObjectsReturned



class CertificateSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Certificate
        fields = '__all__'


class CertificateCreateSerializer(serializers.ModelSerializer):
    # Add a write-only field to handle the phone_number input
    phone_number = serializers.CharField(write_only=True)

    class Meta:
        model = Certificate
        # Fields should be unique_string, price, phone_number which is from User model
        fields = ['unique_string', 'price', 'phone_number']

    def create(self, validated_data):
        # Extract phone_number from the validated data
        phone_number = validated_data.pop('phone_number', None)

        # Find the user based on the provided phone_number
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found for the provided phone number.")

        # Use transaction.atomic to ensure consistency in case of any error
        with transaction.atomic():
            # Create the certificate instance
            certificate = Certificate.objects.create(user=user, **validated_data)

        return certificate
        
    
class CertificateTransferSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    phone_number = serializers.CharField()
    unique_string = serializers.CharField()

    def validate(self, data):
        user_id = data.get('user_id')
        phone_number = data.get('phone_number')
        unique_string = data.get('unique_string')

        if not user_id or not phone_number or not unique_string:
            raise serializers.ValidationError("user_id, phone_number, and unique_string are required.")

        try:
            sender_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("Sender user not found.")

        try:
            recipient_user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError("Recipient user not found.")
        except MultipleObjectsReturned:
            raise serializers.ValidationError("Multiple users found with the same phone number.")

        try:
            certificate = Certificate.objects.get(unique_string=unique_string, user=sender_user)
        except Certificate.DoesNotExist:
            raise serializers.ValidationError("Certificate not found or does not belong to the sender user.")

        if certificate.user == recipient_user:
            raise serializers.ValidationError("Cannot transfer certificate to the same user.")

        # Update the data dictionary with the actual user_id based on the phone_number
        data['user_id'] = recipient_user.id

        return data

    def create(self, validated_data):
        user_id = validated_data['user_id']
        unique_string = validated_data['unique_string']

        with transaction.atomic():
            certificate = Certificate.objects.get(unique_string=unique_string)
            recipient_user = User.objects.get(id=user_id)

            print(f"Before update: Certificate user_id - {certificate.user_id}")

            certificate.user = recipient_user
            certificate.save()
            print(f"After update: Certificate user_id - {certificate.user_id}")

        return certificate