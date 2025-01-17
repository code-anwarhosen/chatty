from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from chat.forms.register import CustomUserCreationForm
from chat.forms.password_change import CustomPasswordChangeForm
from chat.models import Profile

def UserLogin(request):
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

def UserLogout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'You have successfully logged out')
    else:
        messages.error(request, 'You are not logged in')
    return redirect('login')

def UserRegister(request):
    """Handle user registration functionality"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, is_online=True)

            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
        else:
            messages.error(request, 'Registration failed. Please correct the below errors.')
            for error in form.errors:
                messages.error(request, f'{form.errors[error][0]}')
    
    form = CustomUserCreationForm()
    return render(request, 'chat/pages/register.html', {'form': form})

@login_required
def UserProfile(request, username):
    """User details page"""
    if not request.user.is_authenticated:
        messages.info(request, 'You need to log in first to view this page.')
        return redirect('login')

    user = User.objects.filter(username=username).first()
    context = {
        'profile': user
    }
    return render(request, 'chat/pages/UserProfile.html', context)

@login_required
def EditUserProfile(request):
    passwordChangeForm = CustomPasswordChangeForm(request.user)
    context = {
        'passForm': passwordChangeForm
    }
    return render(request, 'chat/pages/EditUserProfile.html', context)


@login_required
def UpdateUserProfile(request):
    user = request.user
    profile = user.profile  # Access the related Profile object

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        
        if first_name: user.first_name = first_name
        if last_name: user.last_name = last_name
        if email: user.email = email
        user.save()

        # Update Profile model fields
        bio = request.POST.get('bio')
        if bio is not None: profile.bio = bio

        avatar = request.FILES.get('avatar')
        if avatar:
            profile.avatar = avatar  # Update avatar only if a new file is uploaded
        profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile', username=user.username)  # Redirect to profile page after updating

    return render(request, 'profile/update_profile.html')

@login_required
def ChangeUserPassword(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user) # keep the user logged in

            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile', username=request.user)
        else:
            for error in form.errors:
                messages.error(request, f'{form.errors[error][0]}')

    return redirect('edit_profile')