from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.utils import timezone
from .models import ShortURL
from .forms import ShortURLForm
from .utils import encode_base62
from django.contrib.auth.forms import UserCreationForm

import os
from django.conf import settings

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    urls = ShortURL.objects.filter(user=request.user)
    return render(request, 'shortener/dashboard.html', {'urls': urls})

@login_required
def create_url(request):
    if request.method == 'POST':
        form = ShortURLForm(request.POST)
        if form.is_valid():
            short = form.save(commit=False)
            short.user = request.user
            short.save()

            short.short_key = encode_base62(short.id)
            short.save()

            return redirect('dashboard')
    else:
        form = ShortURLForm()
    return render(request, 'shortener/create_url.html', {'form': form})

def redirect_url(request, short_key):
    url = get_object_or_404(ShortURL, short_key=short_key)

    if url.expires_at and url.expires_at < timezone.now():
        return render(request, 'shortener/expired.html')

    url.clicks += 1
    url.save()
    return redirect(url.original_url)

@login_required
def edit_url(request, id):
    url = get_object_or_404(ShortURL, id=id, user=request.user)
    form = ShortURLForm(request.POST or None, instance=url)
    if form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'shortener/edit_url.html', {'form': form})

@login_required
def delete_url(request, id):
    url = get_object_or_404(ShortURL, id=id, user=request.user)
    if request.method == 'POST':
        url.delete()
        return redirect('dashboard')
    return render(request, 'shortener/delete_confirm.html', {'url': url})

