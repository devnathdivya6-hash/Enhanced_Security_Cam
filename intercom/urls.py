from django.urls import path
from . import views

urlpatterns = [
    path('record_voice/', views.record_voice, name='record_voice'),
    path('send_message', views.send_message, name='send_message'),
    path("admin-messages", views.admin_view_messages, name="admin_messages"),
    path("my-messages", views.user_messages, name="user_messages"),

]
