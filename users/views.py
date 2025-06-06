from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_backends
from .models import User
from .forms import UserForm, MyUserCreationForm

def login_page(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "User doesn't exist")
            user = None

        if user:
            user = authenticate(request, email=email, password=password)

            if user is not None:
                # Specify backend explicitly
                backend = get_backends()[0]
                login(request, user, backend=f"{backend.__module__}.{backend.__class__.__name__}")
                return redirect('home')
            else:
                messages.error(request, 'Email or Password does not exist')

    context = {'page': page}
    return render(request, 'users/login_register.html', context)

def register_user(request):
    page = 'register'
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            # Manually specify backend when logging in newly created user
            backend = get_backends()[0]  # Get the first backend in your settings
            user.backend = f"{backend.__module__}.{backend.__class__.__name__}"

            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'An error occurred')

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


@login_required(login_url='/users/login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', pk=user.id)
    return render(request, 'users/update_user.html', {'form': form})
