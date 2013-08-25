from django.contrib.auth import authenticate, login
from django.shortcuts import render

def Login(request):
  if ('username' in request.POST) and ('password' in request.POST):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
      if user.is_active:
        login(request, user)
  else:
    return render(request, 'PodCastSite/login.html')

def Logout(request):
  login(request)

