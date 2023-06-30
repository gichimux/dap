from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth import login, authenticate 
from django.contrib.auth.forms import AuthenticationForm 
from core.views  import home
from .models import Profile
from django.contrib.auth.decorators import login_required


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("home")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="auth/register.html", context={"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"Welcome, you are now logged in as {username}.")
				return redirect("profile")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="auth/login.html", context={"login_form":form})


# @login_required
# def my_profile(request):
    
#     profile = Profile.objects.filter(user=request.user)
#     if request.method == 'POST':
#         form = EditProfileForm(request.POST, instance=request.user)
#         profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile) 

#         if form.is_valid() and profile_form.is_valid():
#             form.save()
#             profile_form.save()
#             messages.success(request, 'Your profile has been updated successfully')
#             return redirect(request.META['HTTP_REFERER'])
#     else:
#         form = EditProfileForm(instance=request.user)
#         profile_form = ProfileForm(instance=request.user.profile)
    
#     profiles = Profile.objects.all()
#     context ={
#         'profiles': profiles,
#         'form': form,
#         'profile_form': profile_form
       
#     }
#     return render (request, 'users/profile.html', context )

def logout_request(request):
	logout(request)
	return redirect("/")

def fofo(request):
	context ={

       
    }
	return render (request, '404.html', context )