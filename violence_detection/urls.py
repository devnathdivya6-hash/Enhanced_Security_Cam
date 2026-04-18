# urls.py
from django.urls import path
from .views import upload_video, violence_result

urlpatterns = [
    path('upload_video', upload_video, name='upload_video'),
    path('violence_result/<int:video_id>/', violence_result, name='violence_result'),
]
