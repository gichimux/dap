from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate 
from django.contrib import messages

from django.contrib.auth.forms import AuthenticationForm 

def home(request):
       
    context ={
     
   }
    return render (request, 'app/home.html', context )

def landing(request):
		
    form = AuthenticationForm(request, data=request.POST)

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Welcome, you are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    context ={
        "login_form": form,
    }
    return render (request, 'core/index.html', context )