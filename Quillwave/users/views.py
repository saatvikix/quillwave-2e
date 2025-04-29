from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

from .models import Profile
from .forms import RegisterForm, ProfileForm

import random
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .forms import ForgotPasswordForm, OTPVerificationForm, ResetPasswordForm


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(f"Trying login: {email} | {password}")
        try:
            user = User.objects.get(email=email)
            print(f"Found user: {user}")
            user = authenticate(request, username=user.username, password=password)
            print(f"Authenticated user: {user}")
            if user:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'registration/login.html', {'error': 'Invalid credentials'})
        except User.DoesNotExist:
            print("User not found")
            return render(request, 'registration/login.html', {'error': 'Invalid credentials'})
    return render(request, 'registration/login.html')



def logout_view(request):
    logout(request)
    return redirect('login')


from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, "Registered successfully!")
            return redirect('login')
        else:
            # Debugging output to console
            print("Form errors:", form.errors)
            
    else:
        form = RegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(instance=profile)

    user_posts = request.user.post_set.all()
    post_count = user_posts.count()

    return render(request, 'profile.html', {
        'form': form,
        'posts': user_posts,
        'post_count': post_count,  # ✅ This was missing
        'profile_pic': profile.profile_pic.url if profile.profile_pic else None,
        'location': profile.location,
    })



def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                otp = str(random.randint(100000, 999999))
                request.session['reset_otp'] = otp
                request.session['reset_email'] = email

                send_mail(
                    'Password Reset OTP',
                    f'Your OTP is: {otp}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )

                messages.info(request, 'An OTP has been sent to your email.')
                return redirect('verify_reset_otp')
            else:
                messages.error(request, 'Email not found.')
    else:
        form = ForgotPasswordForm()
    return render(request, 'forgotPassword.html', {'form': form})



def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        original_otp = request.session.get('reset_otp')
        if entered_otp == original_otp:
            messages.success(request, 'OTP verified. You may now reset your password.')
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    return render(request, 'verifyOtp.html')



def reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.session.get('reset_email')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('reset_password')

        try:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password has been reset successfully. Please log in.')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'No user found with that email.')

    return render(request, 'resetPassword.html')


def verify_reset_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        original_otp = request.session.get('reset_otp')
        if entered_otp == original_otp:
            messages.success(request, 'OTP verified. You may now reset your password.')
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    return render(request, 'verifyResetOtp.html')

# For registration (if you're using OTP during registration)
def verify_register_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        original_otp = request.session.get('register_otp')  # You'll need to set this where relevant
        if entered_otp == original_otp:
            messages.success(request, 'OTP verified. Account activated.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    return render(request, 'verifyOtp.html')




def add_info(request):
    return render(request, 'addInfo.html')  

from django.shortcuts import redirect

@login_required
def update_profile(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        profile_pic = request.FILES.get('profile_pic')  # ✅ THIS LINE FIXED

        user_profile = request.user.profile
        user_profile.location = location

        if profile_pic:
            user_profile.profile_pic = profile_pic  # ✅ This should match your model field name

        user_profile.save()

        print("Saved to:", user_profile.profile_pic.url if user_profile.profile_pic else "No image uploaded")  # ✅ debug

        return redirect('profile')
    
    return redirect('add_info')