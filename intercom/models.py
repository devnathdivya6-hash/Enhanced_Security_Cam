from django.db import models
from face.models import Register
# Create your models here.
class InterCom(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)  # Reference User model
    message = models.CharField(max_length=255,null=True, blank=True)
    response = models.CharField(max_length=255, null=True, blank=True)
    date_taken = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}"

    def __str__(self):
        return self.name