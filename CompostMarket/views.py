from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def index(request):
    return render(request, 'index.html')



