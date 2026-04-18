from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('about',views.about),
    path('service',views.service),
    path('team',views.team),
    path('why',views.why),
    path('login/',views.Login),
    path('register',views.register),
    path('logout/',views.logout),
    path('upload/',views.upload),
    path('profile/',views.profile_view),
    path('capture_face_view/', views.capture_face_view, name='capture_face_view'),
    path('scanface', views.recognize_faces_view, name='scanface'),
    path('viewusers',views.viewusers,name='viewusers'),
    path('delete_user/<int:id>/',views.delete_user,name='delete_user'),
]