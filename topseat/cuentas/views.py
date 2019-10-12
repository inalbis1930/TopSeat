# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
#from django.contrib.auth.decorators import login_required


from django.shortcuts import render,redirect
from django.http import HttpResponse
import cuentas

# Create your views here.

def home_cuentas(request):
    return render(request,'cuentas/home.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
			#login
            return redirect('cuentas:login')#('appname:linkname')
    else:
        form = UserCreationForm()
    return render(request,'cuentas/signup.html',{'sgForm':form})


#@login_required
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
			#login
            return redirect('cuentas:signup')#('appname:linkname')
    else:
        form = AuthenticationForm()
    return render(request,'cuentas/login.html',{'lgForm':form})