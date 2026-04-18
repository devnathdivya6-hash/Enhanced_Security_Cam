from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib import auth

import csv
import time
import numpy as np

from .face_utils import capture_face_with_name, train_faces, recognize_faces

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')
def service(request):
    return render(request,'service.html')
def team(request):
    return render(request,'team.html')
def why(request):
    return render(request,'why.html')
def upload(request):
    return render(request,'uploadvid.html')
def Login(request):
    form = LoginForm()
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username)
        print(password)
        
        
        user = authenticate(request, username=username, password=password)
        print(user)

        if user is None:
            messages.error(request, 'Invalid email or password.', extra_tags='log')
            return render(request, 'login.html', {'form': form, 'k': True})
        
        try:
            data = Register.objects.get(username=user.username)
            login(request, user)

            if not data.have_face: 
                return redirect('/capture_face_view')  
            
            messages.success(request, f'Login Successful! Welcome {data.username}', extra_tags='log')
            return redirect('/')  
            
        except Register.DoesNotExist:
            messages.error(request, 'User data not found.', extra_tags='log')
            return redirect('/login')

    return render(request, 'login.html', {'form': form})


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/') 


def register(request):
    if request.method =='POST':
        name=request.POST['uname']
        mail=request.POST['email']
        phone=request.POST['phn']
        passwords=request.POST['pswd']
        Register.objects.create_user(username=name,email=mail,contact_number=phone,password=passwords,usertype="user")
        messages.success(request, f'Register Successful! You can login now', extra_tags='log')
        return redirect('/')
    return render(request,'login.html')





@login_required
def viewusers(request):
    users_list = Register.objects.filter(usertype="user")
    return render(request, 'viewusers.html', {'users': users_list})

@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})



def capture_face_view(request):
    if request.method == 'POST':
        name = request.user.username  
        capture_face_with_name(name)
        train_faces() 
        
        user = Register.objects.get(username=request.user.username)
        user.have_face = True
        user.save()

        messages.success(request, f"Face images for {name} captured and trained successfully.", extra_tags='log')
        return redirect('/') 
    return render(request, 'capture_faces.html') 

@login_required
def recognize_faces_view(request):
    if request.method == 'POST':
        recognize_faces(request)
        with open('face_recognition_log.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([request.user.username, "Face recognized", time.strftime("%Y-%m-%d %H:%M:%S")])
        messages.success(request, "Face recognition completed and logged to csv.",extra_tags='log')
    return render(request, 'recognize_faces.html') 
    
@login_required
def delete_user(request,id):
    user = Register.objects.get(id=id)
    user.delete()
    messages.success(request,'User deleted successfully',extra_tags='log')
    return redirect('viewusers')