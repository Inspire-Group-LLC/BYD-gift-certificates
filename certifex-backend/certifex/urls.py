
from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView
from users.views import UserCreateApiView, CustomAuthToken, UserLoginApiView
from rest_framework.authtoken.views import obtain_auth_token



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/certificates/', include('certificates.urls')),
    path('signup/', UserCreateApiView.as_view(), name='user-signup'),
    path('login/', UserLoginApiView.as_view(), name='user-login'),


    path('api_schema/', get_schema_view(title='Projects API Documentation', description='Guide for the REST API'), name='projects_api_schema'),
    path('swagger/', TemplateView.as_view(
        template_name='docs.html',
        extra_context={'schema_url':'projects_api_schema'}
        ), name='swagger'),
]
