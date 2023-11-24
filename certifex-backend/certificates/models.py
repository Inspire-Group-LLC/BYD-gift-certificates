from django.db import models
from users.models import User
# Create your models here.


class Certificate(models.Model):
    unique_string = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    price = models.FloatField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.unique_string

