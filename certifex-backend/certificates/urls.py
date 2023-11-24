from django.urls import path
from .views import CertificatesListApiView, CertificatesApiDetailView, CertificateTransferApiView, CertificateCreateAPIView

urlpatterns = [
    path('', CertificatesListApiView.as_view()),
    path('create/', CertificateCreateAPIView.as_view()),
    path('detail/<int:pk>/', CertificatesApiDetailView.as_view()),
    path('transfer/', CertificateTransferApiView.as_view(), name='certificates-transfer'),

]

