from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth import login as auth_login, logout as auth_logout

from .forms import CustomAuthenticationForm, CustomUserCreationForm

from django.contrib.auth import get_user_model

User = get_user_model()


@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {
        'form': form,
    })


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('/')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {
        'form': form,
    })


def logout(request):
    auth_logout(request)
    return redirect('/')


@require_GET
def user_page(request, user_id):
    user_info = get_object_or_404(User, id=user_id)
    return render(request, 'accounts/user_page.html', {
        'user_info': user_info,
    })


def follow(request, user_id):
    follower = request.user
    following = get_object_or_404(User, id=user_id)

    if follower != following:
        if follower.followings.filter(id=follower.id).exists():
            following.followers.remove(follower)
        else:
            following.followers.add(follower)
    return redirect(following)
