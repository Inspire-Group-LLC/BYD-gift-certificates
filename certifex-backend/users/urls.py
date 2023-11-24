from django.urls import path
from .views import UserListApiView, UserApiDetailView, UserCreateApiView

urlpatterns = [
    path('', UserListApiView.as_view()),
    # path('create/', UserCreateApiView.as_view()),
    path('detail/<int:pk>/', UserApiDetailView.as_view()),
]

