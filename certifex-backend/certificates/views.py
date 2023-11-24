from rest_framework import generics, status
from .models import Certificate
from .serializers import CertificateSerializer, CertificateCreateSerializer, CertificateTransferSerializer
from rest_framework.response import Response
from users.models import User
from rest_framework import filters
from django.contrib.auth.hashers import make_password
from rest_framework import serializers


class CertificatesListApiView(generics.ListAPIView):
    serializer_class = CertificateSerializer
    filterset_fields = ("user__full_name",)
    filter_backends = [filters.SearchFilter]
    search_fields = ["user__full_name", "unique_string"]

    def get_queryset(self):
        user_id_param = self.request.query_params.get("userid")
        user = self.request.user

        # If user_id is provided in the request, filter certificates by that user_id
        if user_id_param:
            try:
                user_id_param = int(user_id_param)
                # Check if the provided user ID is a valid user
                specified_user = User.objects.get(pk=user_id_param)
                if specified_user.is_superuser:
                    # If the specified user is a superuser, return all certificates
                    queryset = Certificate.objects.all()
                else:
                    # If the specified user is not a superuser, return their certificates
                    queryset = Certificate.objects.filter(user=specified_user)
            except (ValueError, User.DoesNotExist):
                return Certificate.objects.none()  # Return an empty queryset if user_id is not a valid integer or user not found

        # If the user is a superuser, show all certificates
        elif user.is_superuser:
            queryset = Certificate.objects.all()

        # If the user is not a superuser, show only their certificates
        else:
            queryset = Certificate.objects.filter(user=user)

        # Apply sorting logic based on the 'order' query parameter
        order_by = self.request.query_params.get("order", "desc")
        valid_orders = ["asc", "desc"]
        if order_by not in valid_orders:
            order_by = "desc"

        if order_by == "asc":
            queryset = queryset.order_by("created_at")
        else:
            queryset = queryset.order_by("-created_at")

        return queryset

    def perform_create(self, serializer):
        # Set the user to the authenticated user during the creation process
        serializer.save(user=self.request.user)

class CertificateCreateAPIView(generics.CreateAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateCreateSerializer

    def perform_create(self, serializer):
        serializer.save()

# GET,PUT,DELETE methods
class CertificatesApiDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer


class CertificateTransferApiView(generics.CreateAPIView):
    serializer_class = CertificateTransferSerializer
    queryset = Certificate.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = CertificateTransferSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        try:
            certificate = serializer.save()
        except serializers.ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        response_data = {
            "user_id": certificate.user.id if certificate.user else None,
            "phone_number": serializer.validated_data['phone_number'],
            "unique_string": serializer.validated_data['unique_string'],
        }

        return Response(response_data, status=status.HTTP_200_OK)