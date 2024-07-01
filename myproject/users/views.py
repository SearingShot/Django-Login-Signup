from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.user_type == 'patient':
                return redirect('patient_dashboard')
            else:
                return redirect('doctor_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})


def home(request):
    return render(request, 'users/home.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.user_type == 'patient':
                return redirect('patient_dashboard')
            else:
                return redirect('doctor_dashboard')
    return render(request, 'users/login.html')

@login_required
def patient_dashboard(request):
    if request.user.user_type != 'patient':
        return redirect('doctor_dashboard')
    return render(request, 'users/patient_dashboard.html')

@login_required
def doctor_dashboard(request):
    if request.user.user_type != 'doctor':
        return redirect('patient_dashboard')
    return render(request, 'users/doctor_dashboard.html')
