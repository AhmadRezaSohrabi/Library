from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from user.models import User

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('home')
    
    return render(request, 'registration/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in
            login(request, user)
            return redirect('home')
        else:
            # Invalid login credentials
            error_message = "Invalid username or password."
            return render(request, 'registration/login.html', {'error_message': error_message})

    return render(request, 'registration/login.html')