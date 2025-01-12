from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from chat.forms.register import CustomUserCreationForm
from chat.models import Profile

def UserLoginView(request):
    """Handle user login functionality"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in')
            return redirect('home')
        else:
            messages.error(request, 'Invalid Username or Password!')
    return render(request, 'chat/pages/login.html')

def UserLogoutView(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'You have successfully logged out')
    else:
        messages.error(request, 'You are not logged in')
    return redirect('login')

def UserRegisterView(request):
    """Handle user registration functionality"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, is_online=True)

            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('profile', username=user.username)
        else:
            messages.error(request, 'Registration failed. Please correct the below errors.')
            for error in form.errors:
                messages.error(request, f'{error}: {form.errors[error][0]}')
    
    form = CustomUserCreationForm()
    return render(request, 'chat/pages/register.html', {'form': form})