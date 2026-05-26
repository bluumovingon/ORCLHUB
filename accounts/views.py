from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from artikel.models import Artikel
from galeri.models import Helm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Selamat datang kembali, {user.username}! 🏁')
                next_url = request.GET.get('next', 'accounts:dashboard')
                return redirect(next_url)
        else:
            messages.error(request, 'Username atau password salah. Silakan coba lagi.')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Akun berhasil dibuat! Selamat bergabung, {user.username}! 🚀')
            return redirect('accounts:dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    """Logout and redirect to login page."""
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Anda telah berhasil logout. Sampai jumpa di paddock! 👋')
    return redirect('accounts:login')


@login_required(login_url='accounts:login')
def dashboard_view(request):
    """Dashboard - protected view, only accessible by authenticated users."""
    # Collect stats for dashboard
    try:
        total_artikel = Artikel.objects.count()
    except Exception:
        total_artikel = 0

    try:
        total_galeri = Helm.objects.count()
    except Exception:
        total_galeri = 0

    try:
        total_users = User.objects.count()
    except Exception:
        total_users = 0

    try:
        recent_artikel = Artikel.objects.order_by('-id')[:5]
    except Exception:
        recent_artikel = []

    context = {
        'total_artikel': total_artikel,
        'total_galeri': total_galeri,
        'total_users': total_users,
        'recent_artikel': recent_artikel,
    }
    return render(request, 'accounts/dashboard.html', context)
