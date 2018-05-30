from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse

from accounts.forms import (
    RegistrationForm,
    EditProfileForm,
    ChangePassword
)

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.decorators import login_required

from home.models import BlogPost

def register(request):
    
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST.get('username')
            password = request.POST.get('password1')
            user = authenticate(
                request,
                username=username,
                password=password
            )
            login(request, user)
            return redirect(reverse('home:home'))
    else:
        form = RegistrationForm()
    args = {'form': form}
    return render(request, 'accounts/reg_form.html', args)




def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)
    

def view_profile(request, pk=None):
    storage = messages.get_messages(request)
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user, 'message': storage}
    return render(request, 'accounts/profile.html', args)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:view_profile'))
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)

def change_password(request):
    if request.method == 'POST':
        form = ChangePassword(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your new password has been saved.')
            update_session_auth_hash(request,form.user)
            return redirect(reverse('accounts:view_profile'))

    else:
        form = ChangePassword(user=request.user)
    args = {'form': form}
    return render(request,'accounts/change_password.html', args)


