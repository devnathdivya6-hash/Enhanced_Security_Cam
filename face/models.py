from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Register(AbstractUser):
    contact_number=models.CharField(max_length=255,null=True)
    usertype=models.CharField(max_length=255,default="admin")
    have_face = models.BooleanField(default=False)
    
