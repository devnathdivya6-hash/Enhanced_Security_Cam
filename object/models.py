from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Detection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # The user who uploaded the image
    image = models.ImageField(upload_to='uploads/')  # The uploaded image
    result = models.TextField()  # Detected objects
    output_image = models.ImageField(upload_to='output/')  # Output image with annotations
    timestamp = models.DateTimeField(auto_now_add=True)  # When the detection happened
